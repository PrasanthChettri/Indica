import os
from dotenv import load_dotenv

load_dotenv()

import os
import yfinance as yf
import pprint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prettytable import PrettyTable
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import requests
import json
import pandas as pd
from news import get_announcements




class Gemini:
    MODEL_NAME: str | None  = os.getenv("MODEL_NAME")
    TEMPERATURE: str | None = os.getenv("TEMPERATURE")

    def __init__(self):
        if self.__class__.MODEL_NAME is None:
            raise ValueError("MODEL_NAME is not set")
        if self.__class__.TEMPERATURE is None:
            raise ValueError("TEMPERATURE is not set")
        self.llm = ChatGoogleGenerativeAI(model=self.__class__.MODEL_NAME, temperature=float(self.__class__.TEMPERATURE))

    def get_llm(self):
        return self.llm

    def get_chain(self, prompt: PromptTemplate) -> LLMChain:
        return LLMChain(llm=self.llm, prompt=prompt)


    