from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:Spl54Q4fcTTVfUmh@cluster0.mtfjbub.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

def get_desc(collection_name: list, section_number: str):
    
    sections = [sec.strip() for sec in section_number.split(",")]
    db = client['Indian_Acts']
    section_desc = []
    for col in collection_name:
        collection = db[col]
        
        query = {'Section_Number': {'$in': sections}}
        results = collection.find(query)

        section_desc.append(res['Description'] for res in results)
    
    return section_desc
    
ff = get_desc(['IPC'], "320")
print(ff[0])