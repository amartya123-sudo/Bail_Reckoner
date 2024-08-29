import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from google import generativeai as genai
from time import time

uri = "mongodb+srv://admin:Spl54Q4fcTTVfUmh@cluster0.mtfjbub.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

client = MongoClient(uri, server_api=ServerApi('1'))

class Reckoner:
    def __init__(self) -> None:
        pass

    def llm(instruction:str):
        return genai.GenerativeModel(model='gemini-1.5-flash', system_instruction=instruction)
    

    def fetch(collection_name: str, section_number:str):
        db = client['Indian_Acts']
        collection = db[collection_name]
        section_desc = collection.find({'Section_Number':section_number})

        return section_desc
        
    def parse():
        


"""
304A - Bailable Section,
Where 304A & 326
"""

