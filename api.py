from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from main import Reckoner

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



@app.post("/submit_bail_application/")
async def submit_bail_application(request: Request):
    
    application = await request.json()
    reckoner = Reckoner()
    
    print(application)
    
    selected_act = application.get('case_details', {}).get('Acts of Offence', [])
    sections_input = application.get('case_details', {}).get('sections_of_offence', [])
    print(type(selected_act))
    print(type(sections_input))

    # Fetch, parse, and process the data
    acts = reckoner.fetch(selected_act, sections_input)
    parsed = reckoner.parse(acts)
    offences = reckoner.llm_parser(parsed)
    application['offences'] = offences
    # Evaluate the final result
    print(application)
    result = reckoner.evaluator(application)
    print(result)
    return result