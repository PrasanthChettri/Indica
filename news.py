import asyncio
from typing import List
import requests
import json
import pdfplumber
import io
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import prompts
from dotenv import load_dotenv, find_dotenv
from services.arequest import ARequest

load_dotenv(find_dotenv())
import os

llm = GoogleGenerativeAI(model="models/gemini-2.5-flash-lite-preview-06-17", temperature=0.8)
api_key = os.getenv("INDIA_NEWS_API_KEY")
    

async def get_pdf_blob(link):
    """
    Downloads a PDF from the given link and returns its binary content (blob).
    """
    if link is None :
        return None
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Accept": "application/pdf",
            "Referer": "https://www.bseindia.com/",
        }
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        if response.headers.get("Content-Type", "").lower() != "application/pdf":
            print("Warning: The downloaded file may not be a PDF.")
        return response.content
    except Exception as e:
        print(f"Error downloading PDF: {str(e)}")
        return None

async def extract_pdf_text(pdf_blob):
    """
    Extracts text and tables from a PDF blob using pdfplumber.
    Returns a dictionary with 'text' and 'tables' keys.
    """
    try:
        # Convert blob to file-like object
        pdf_file = io.BytesIO(pdf_blob)
        
        extracted_data = {
            'text': '',
            'tables': []
        }
        
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract text
                page_text = page.extract_text()
                if page_text:
                    extracted_data['text'] += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                
                # Extract tables
                page_tables = page.extract_tables()
                if page_tables:
                    for table_num, table in enumerate(page_tables):
                        table_data = {
                            'page': page_num + 1,
                            'table_number': table_num + 1,
                            'data': table
                        }
                        extracted_data['tables'].append(table_data)
        
        return extracted_data
    except Exception as e:
        print(f"Error extracting PDF content: {str(e)}")
        return None

def format_table_as_csv(table: List[List[str]]):
    """
    Formats a table as readable text for LLM consumption.
    """
    if not table or not table[0]:
        return "Empty table"
    return "\n".join(map(lambda x: ",".join(x), table))


async def extract_announcement_data(announcement):
    item = dict(announcement)  # shallow copy
    pdf_blob = await get_pdf_blob(item.get('link', None))
    if pdf_blob:
        extracted_data = await extract_pdf_text(pdf_blob)
        if extracted_data:
            print(f"Extracted text from PDF: {extracted_data['text'][:200]}...")  # Print first 200 chars
            print(f"Found {len(extracted_data['tables'])} tables in PDF")
            item['pdf_content'] = extracted_data['text']
            item['tables'] = extracted_data['tables']
    return item

async def get_announcements(stock_name):
    stock_name = stock_name.upper().split(".")[0]
    response = requests.get(
        "https://stock.indianapi.in/recent_announcements",
        params={
        "stock_name": stock_name,
        },
        headers={
            "X-Api-Key": api_key
        }
    )
    announcement_data = response.json()
    announcement_data = await asyncio.gather(*[extract_announcement_data(i) for i in announcement_data])
    parsed_data = ""
    for title, link, date, pdf_content, table in map(lambda x: x.values(), announcement_data) :
        parsed_data += f"""Article Title: {title}
Article Link: {link}
Aricle Date: {date}\n
Article PDF Content: {pdf_content}
Article Tables: {format_table_as_csv(table)}
"""
    print(parsed_data)
    # Create a prompt for Gemini to analyze the announcements

    # Create LLM chain for announcement analysis
    announcement_chain = LLMChain(llm=llm, prompt=prompts.NEWS_PROMPT)

    # Get AI analysis of announcements
    try:
        announcement_analysis = await announcement_chain.arun(
            stock_name=stock_name,
            announcement_data=parsed_data
        )
        return announcement_analysis
    except Exception as e:
        print(f"Error analyzing announcements: {str(e)}")
        return None

if __name__ == "__main__" :
    s = asyncio.run(get_announcements('IRCTC.NS'))
    print(s)
