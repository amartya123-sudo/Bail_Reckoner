import streamlit as st
from .main import Reckoner

st.set_page_config(page_title="Bail Reckoner", layout="wide",page_icon="Law_compliant.png")
st.title("⚖️ Bail Reckoner")
# st.markdown(
#     """
#     <h1 style="display:flex; align-items:center;">
#         <img src="Law_compliant.png" width="30" style="margin-right: 10px;">
#         Bail Reckoner
#     </h1>
#     """,
#     unsafe_allow_html=True
# )

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

selected = st.selectbox("Select an Act", list(acts.keys()))
selected_act = acts[selected]

sections_input = st.text_input("Enter Sections (comma-separated)", placeholder="Enter Section of Offence")

age = st.text_input("Age")
gender = st.radio("Gender", ["Male", "Female", "Other"])
convictions = st.text_input("Previous Convictions")
repeat_offender = st.radio("Repeat Offender", ["Yes", "No"])
public_offences = st.text_area("Nature of the Offense (Public Safety)")
violent_behaviour = st.radio("Violent Behavior", ["Yes", "No"])
gang = st.text_input("Gang Affiliations")
previous_order = st.text_input("Previous Compliance with Court Orders")
court_attendence = st.text_input("History of Court Attendance")
health_condition = st.radio("Health Conditions", ["Yes", "No"])
dependent_members = st.text_input("Dependent Family Members")
if gender=="Female":
    pregnant = st.radio("Pregnant (if applicable)", ["Not applicable", "Yes", "No"])
else:
    pregnant = "No"
reckoner = Reckoner()
acts = reckoner.fetch(selected_act,sections_input)
parsed = reckoner.parse(acts)
offences = reckoner.llm_parser(parsed)

if st.button("Generate Recommendation"):
    inputs = {
        "age": age,
        "gender": gender,
        "offences": offences,
        "convictions": convictions,
        "repeat_offender": repeat_offender,
        "public_offences": public_offences,
        "violent_behaviour": violent_behaviour,
        "gang": gang,
        "previous_order": previous_order,
        "court_attendence": court_attendence,
        "health_condition": health_condition,
        "dependent_members": dependent_members,
        "pregnant": pregnant,
    }
    result = reckoner.evaluator(inputs)
    st.text_area("Bail Assessment Recommendation", result, height=300)

