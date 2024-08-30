import os
import regex as re
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from google import generativeai as genai
from time import time
from prompt_library import Prompt

uri = "mongodb+srv://admin:Spl54Q4fcTTVfUmh@cluster0.mtfjbub.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

client = MongoClient(uri, server_api=ServerApi('1'))

class Reckoner:
    def __init__(self) -> None:
        pass

    def llm(self, instruction:str):
        return genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)
    

    def fetch(self, collection_name: str, section_number: str):
        sections = [sec.strip() for sec in section_number.split(",")]
        db = client['Indian_Acts']
        collection = db[collection_name]
        
        query = {'Section_Number': {'$in': sections}}
        results = collection.find(query)

        section_desc = [res['Description'] for res in results]
        
        return section_desc


    def parse(self, text:str):
        model = self.llm(instruction=Prompt.ParseInstruction)
        parsed_response = model.generate_content(Prompt.ParsePrompt(text)).text
        json_string = re.search(r'\{.*\}', parsed_response, re.DOTALL)
        return json.loads(json_string.group(0))
    
    def llm_parser(self, data:dict):
        results = {}
        for collection_name, sections in data.items():
            collection = client['Indian_Acts'][collection_name]
            if sections: 
                query = {'Section_Number': {'$in': sections}}
            
            result = collection.find(query)
            response = [res for res in result]
        
        return response
    
    def evaluator(self, input: dict):
        model = self.llm(instruction=Prompt.evaluator)
        return model.generate_content(Prompt.evalPrompt(input)).text

    # def main(self):
    #     # section = self.fetch("PMLA", "11")
    #     return self.llm_parser()


# reckoner = Reckoner()
# print(reckoner.main())


"""
304A - Bailable Section,
Where 304A & 326
"""

