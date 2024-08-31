from fastapi import FastAPI
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


class PersonalInformation(BaseModel):
    age: int
    gender: str


class CaseDetails(BaseModel):
    incident_brief: str = Field(..., alias="Incident Brief")
    acts: List[str] = Field(..., alias="Offense Acts")
    offence_section: str = Field(
        ..., alias="Sections under which the offender was arrested"
    )


class BailApplicationHistory(BaseModel):
    previous_bail_application: str = Field(..., alias="Any previous bail application?")
    terms_conditions: Optional[str] = Field(None, alias="Terms & Conditions")
    grounds_rejection: Optional[str] = Field(None, alias="Grounds for Rejection")
    court_name: Optional[str] = Field(
        None, alias="Court where the application was decided"
    )


class CriminalHistory(BaseModel):
    previous_case: str = Field(..., alias="Any other previous case?")
    offence_acts: str = Field(..., alias="Previous offence Acts")
    sections_offence: Optional[List[str]] = Field(None, alias="Sections of previous offence")


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
    reckoner = Reckoner()
    selected_act = application.case_details.acts
    sections_input = application.case_details.offence_section
    acts = reckoner.fetch(selected_act, sections_input)
    parsed = reckoner.parse(acts)
    offences = reckoner.llm_parser(parsed)
    inputs = {
        "age": application.personal_information.age,
        "gender": application.personal_information.gender,
        "acts": application.case_details.acts,
        "offence_section": offences,
        "previous_bail_application": application.bail_application_history.previous_bail_application,
        "terms_conditions": application.bail_application_history.terms_conditions,
        "grounds_rejection": application.bail_application_history.terms_conditions,
        "court_name": application.bail_application_history.court_name,
        "previous_case": application.criminal_history.previous_case,
        "offence_acts": application.criminal_history.offence_acts,
        "sections_offence": application.criminal_history.sections_offence,
        "medical_condition": application.health_information.medical_condition,
    }
    return reckoner.evaluator(inputs)
