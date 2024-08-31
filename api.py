from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class PersonalInformation(BaseModel):
    age: int
    gender: str

class CaseDetails(BaseModel):
    incident_brief: str = Field(..., alias="Incident Brief")
    sections_arrested: List[str] = Field(..., alias="Sections under which the offender was arrested")

class BailApplicationHistory(BaseModel):
    previous_bail_application: bool = Field(..., alias="Any previous bail application?")
    terms_conditions: Optional[str] = Field(None, alias="Terms & Conditions")
    grounds_rejection: Optional[str] = Field(None, alias="Grounds for Rejection")
    court_name: Optional[str] = Field(None, alias="Court where the application was decided")

class CriminalHistory(BaseModel):
    previous_case: bool = Field(..., alias="Any other previous case?")
    sections_offense: Optional[List[str]] = Field(None, alias="Sections of offense")

class HealthInformation(BaseModel):
    medical_condition: Optional[str] = Field(None, alias="Any medical condition?")

class BailApplication(BaseModel):
    personal_information: PersonalInformation
    case_details: CaseDetails
    bail_application_history: Optional[BailApplicationHistory]
    criminal_history: CriminalHistory
    health_information: HealthInformation

@app.post("/submit_bail_application/")
async def submit_bail_application(application: BailApplication):
    return {"message": "Bail application received successfully!", "data": application}

