import json
import re
from datetime import datetime

def extract_notebook_content_simple():
    """
    Extract content from exp.ipynb without external dependencies
    """
    
    # Read the notebook file
    try:
        with open('exp.ipynb', 'r') as f:
            notebook_content = f.read()
    except FileNotFoundError:
        return {"error": "exp.ipynb file not found"}
    
    # Extract code cells and outputs
    extracted_data = {
        "source": "exp.ipynb",
        "extraction_timestamp": datetime.now().isoformat(),
        "cells": []
    }
    
    # Simple parsing of notebook content
    # Look for cell patterns
    cell_pattern = r'Cell \d+:\n```\n(.*?)\n```'
    output_pattern = r'Cell \d+ output.*?```\n(.*?)\n```'
    
    cells = re.findall(cell_pattern, notebook_content, re.DOTALL)
    outputs = re.findall(output_pattern, notebook_content, re.DOTALL)
    
    for i, (cell, output) in enumerate(zip(cells, outputs)):
        extracted_data["cells"].append({
            "cell_number": i + 1,
            "code": cell.strip(),
            "output": output.strip()[:1000] + "..." if len(output) > 1000 else output.strip()
        })
    
    return extracted_data

def create_llm_prompt_simple(extracted_data):
    """
    Create a simple prompt for LLM analysis
    """
    
    prompt = f"""
    Analyze the following Jupyter notebook content and provide insights:

    === NOTEBOOK CONTENT ===
    Source: {extracted_data['source']}
    Extracted: {extracted_data['extraction_timestamp']}

    """
    
    for cell in extracted_data.get('cells', []):
        prompt += f"""
    === CELL {cell['cell_number']} ===
    CODE:
    {cell['code']}
    
    OUTPUT:
    {cell['output']}
    
    """
    
    prompt += """
    === ANALYSIS REQUEST ===
    Please analyze this notebook content and provide:
    
    1. **Code Analysis**: What does each cell do? What libraries and APIs are being used?
    2. **Data Analysis**: What financial data is being analyzed? What insights can be drawn?
    3. **Technical Indicators**: What technical analysis is being performed?
    4. **News Integration**: How is news data being integrated and processed?
    5. **Recommendations**: What improvements or insights can you suggest?
    6. **Potential Issues**: Are there any concerns with the code or data handling?
    
    Provide a comprehensive analysis in a structured format.
    """
    
    return prompt

def save_for_llm_injection():
    """
    Main function to extract and prepare content for LLM injection
    """
    print("Extracting notebook content for LLM injection...")
    
    # Extract content
    extracted_data = extract_notebook_content_simple()
    
    # Save extracted data
    with open('notebook_content_for_llm.json', 'w') as f:
        json.dump(extracted_data, f, indent=2)
    
    print("✓ Notebook content extracted and saved to 'notebook_content_for_llm.json'")
    
    # Create LLM prompt
    prompt = create_llm_prompt_simple(extracted_data)
    
    # Save prompt
    with open('llm_prompt_simple.txt', 'w') as f:
        f.write(prompt)
    
    print("✓ LLM prompt created and saved to 'llm_prompt_simple.txt'")
    
    # Create a summary for quick review
    summary = {
        "total_cells": len(extracted_data.get('cells', [])),
        "libraries_used": extract_libraries(extracted_data),
        "apis_used": extract_apis(extracted_data),
        "data_sources": extract_data_sources(extracted_data)
    }
    
    with open('notebook_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("✓ Notebook summary saved to 'notebook_summary.json'")
    
    print("\n=== READY FOR LLM INJECTION ===")
    print("You can now use the content in 'llm_prompt_simple.txt' with any LLM service.")
    print("The prompt contains all the notebook content formatted for analysis.")
    
    return extracted_data, prompt

def extract_libraries(extracted_data):
    """Extract libraries used in the notebook"""
    libraries = set()
    for cell in extracted_data.get('cells', []):
        code = cell['code']
        # Look for import statements
        import_pattern = r'import (\w+)'
        from_pattern = r'from (\w+)'
        
        imports = re.findall(import_pattern, code)
        froms = re.findall(from_pattern, code)
        
        libraries.update(imports)
        libraries.update(froms)
    
    return list(libraries)

def extract_apis(extracted_data):
    """Extract APIs used in the notebook"""
    apis = set()
    for cell in extracted_data.get('cells', []):
        code = cell['code']
        # Look for API endpoints
        url_pattern = r'https?://[^\s\'"]+'
        urls = re.findall(url_pattern, code)
        apis.update(urls)
    
    return list(apis)

def extract_data_sources(extracted_data):
    """Extract data sources mentioned in the notebook"""
    sources = set()
    for cell in extracted_data.get('cells', []):
        code = cell['code']
        # Look for ticker symbols
        ticker_pattern = r'["\']([A-Z]{1,5}\.[A-Z]{2})["\']'
        tickers = re.findall(ticker_pattern, code)
        sources.update(tickers)
        
        # Look for stock names
        stock_pattern = r'["\']([A-Z]{2,10})["\']'
        stocks = re.findall(stock_pattern, code)
        sources.update(stocks)
    
    return list(sources)

if __name__ == "__main__":
    save_for_llm_injection() 