import streamlit as st
from main import Reckoner

reckoner = Reckoner()

st.title("⚖️ Bail Reckoner")

acts = {
    "Select an Act": None,
    "THE BHARATIYA NYAYA SANHITA, 2023": "BNS",
    "THE BHARATIYA NAGARIK SURAKSHA SANHITA, 2023":"BNSS",
    "THE CODE OF CRIMINAL PROCEDURE, 1973":"CrPC",
    "THE PROTECTION OF WOMEN FROM DOMESTIC VIOLENCE ACT, 2005":"DVA",
    "THE INDIAN PENAL CODE":"IPC",
    "THE INDECENT REPRESENTATION OF WOMEN (PROHIBITION) ACT, 1986":"IRWA",
    "THE IMMORAL TRAFFIC (PREVENTION) ACT, 1956":"ITA",
    "THE INFORMATION TECHNOLOGY ACT, 2000":"ITAct",
    "THE JUVENILE JUSTICE (CARE AND PROTECTION OF CHILDREN) ACT, 2015":"JJA",
    "THE NATIONAL INVESTIGATION AGENCY ACT, 2008":"NIA",
    "THE NATIONAL SECURITY ACT, 1980":"NSA",
    "THE PREVENTION OF CORRUPTION ACT, 1988":"PCA",
    "THE PREVENTION OF MONEY-LAUNDERING ACT, 2002":"PMLA",
    "THE PROTECTION OF CHILDREN FROM SEXUAL OFFENCES ACT, 2012":"POSCO",
    "THE SCHEDULED CASTES AND THE SCHEDULED TRIBES (PREVENTION OF ATROCITIES) ACT, 1989":"SCSTAct",
    "THE UNLAWFUL ACTIVITIES (PREVENTION) ACT, 1967":"UAPA"
}

formData = {}

age = st.text_input("Age")
gender = st.radio("Gender", options=["Male", "Female"])

if age and gender:
    formData['personal_information'] = {
        "age": int(age),
        "gender": gender,
    }

incidentBrief = st.text_area("Incident Brief")
sectionsOffense = st.multiselect("Acts of Offence", acts.keys())
sections = st.text_input("Enter Sections (comma-separated)", placeholder="Enter Section of Offence")

if incidentBrief and sectionsOffense:
    formData['case_details'] = {
        "Acts of Offence": sectionsOffense,
        "sections_of_offence": sections,
        "Incident Brief": incidentBrief,
    }
previousBail = st.radio("Any previous bail application?", options=["Yes", "No"])
if previousBail == 'Yes':
    bailOutcome = st.radio("Outcome", options=["Allowed", "Not Allowed"])
    allowedTerms = st.text_area("Terms & Conditions") if bailOutcome == 'Allowed' else None
    groundsRejection = st.text_area("Grounds for Rejection") if bailOutcome == 'Not Allowed' else None
    courtName = st.text_input("Court where the application was decided")

    formData['bail_application_history'] = {
        "Any previous bail application?": previousBail,
        "Outcome": bailOutcome,
        **({"Terms & Conditions": allowedTerms} if allowedTerms else {}),
        **({"Grounds for Rejection": groundsRejection} if groundsRejection else {}),
        "Court where the application was decided": courtName or None,
    }

otherCase = st.radio("Any other previous case?", options=["Yes", "No"])
if otherCase == 'Yes':
    prevsectionsOffense = st.multiselect("Previous Acts of Offence", list(acts.keys()))
    prevsections = st.text_input("Previous Section of Offence", placeholder="Enter Section of Offence")

    formData['criminal_history'] = {
        "Any other previous case?": otherCase,
        "Prev Acts of Offence": prevsectionsOffense,
        "Prev Section of Offence": prevsections,
    }

medicalCondition = st.text_area("Any medical condition?")
if medicalCondition:
    formData['health_information'] = {
        "Any medical condition?": medicalCondition,
    }

submit = st.button("Check Recommendation") 

if submit:
    with st.spinner("Processing..."):
        act = formData.get('case_details', {}).get('Acts of Offence', [])
        section = formData.get('case_details', {}).get('sections_of_offence', [])
        acts = reckoner.fetch(act, section)
        parsed = reckoner.parse(acts)
        offences = reckoner.llm_parser(parsed)
        formData["criminal_history"] = offences
        result = reckoner.evaluator(formData)
        st.write(result)
