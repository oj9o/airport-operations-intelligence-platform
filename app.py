import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_incident(incident):
    prompt = f"""
You are an airport operations expert.

Classify this airport incident.

Incident:
{incident}

Return only:

Category:
Risk:
Affected Departments:
"""
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    return response.output_text

def generate_executive_summary(incident):
    prompt = f"""
You are the Director of Airport Operations.

Create a professional executive briefing.

Incident:
{incident}

Return:

Situation Summary:
Operational Impact:
Immediate Actions:
Executive Recommendation:
"""
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    return response.output_text

st.set_page_config(
    page_title="Airport Operations Intelligence Platform",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Airport Operations Intelligence Platform")

st.sidebar.title("Airport AI Navigation")

page = st.sidebar.radio(
    "Menu",
    ["Analyze Incident", "Knowledge Base", "System Status"]
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("System Status", "Operational")
col2.metric("Active Incidents", "1")
col3.metric("AI Engine", "Online")
col4.metric("Knowledge Base", "Connected")

if page == "Analyze Incident":

    st.subheader("Incident Analysis Center")

    incident_type = st.selectbox(
        "Incident Type",
        [
            "Flight Delay",
            "Weather Event",
            "Security Incident",
            "Aircraft Accident",
            "Airspace Closure",
            "Technical Issue",
            "Medical Emergency",
            "Other"
        ]
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("✈ Flight Delay"):
            st.session_state["incident"] = "Flight delayed due to weather conditions"
        if st.button("🌫 Weather Disruption"):
            st.session_state["incident"] = "Severe fog affecting airport operations"

    with c2:
        if st.button("⚠ Airspace Closure"):
            st.session_state["incident"] = "Regional airspace closure affecting flights"
        if st.button("🔒 Security Incident"):
            st.session_state["incident"] = "Unauthorized access detected at terminal"

    with c3:
        if st.button("🚨 Aircraft Accident"):
            st.session_state["incident"] = "Aircraft crashed during landing"
        if st.button("🩺 Medical Emergency"):
            st.session_state["incident"] = "Passenger medical emergency onboard aircraft"

    question = st.text_area(
        "Describe what happened",
        value=st.session_state.get("incident", ""),
        height=120
    )

    if st.button("Analyze Incident"):

        q = question.lower()

        risk_level = "Low"
        category = incident_type

        if any(word in q for word in ["crash","crashed","fatal","plane crash"]):
            risk_level = "Critical"
            category = "Aircraft Accident"
        elif any(word in q for word in ["war","missile","military"]):
            risk_level = "High"
            category = "Regional Crisis"
        elif any(word in q for word in ["security","bomb","terror","unauthorized"]):
            risk_level = "High"
            category = "Security Incident"
        elif any(word in q for word in ["delay","fog","storm","weather"]):
            risk_level = "Medium"
            category = "Weather Disruption"
        ai_result = classify_incident(question)
        executive_summary = generate_executive_summary(question)

        d1, d2, d3, d4 = st.columns(4)

        d1.metric("System Status", "Operational")

        if risk_level == "Critical":
            d2.error("🔴 Critical Risk")
        elif risk_level == "High":
            d2.warning("🟠 High Risk")
        elif risk_level == "Medium":
            d2.info("🟡 Medium Risk")
        else:
            d2.success("🟢 Low Risk")

        d3.metric("Category", category)

        if risk_level == "Critical":
            d4.error("P1")
        elif risk_level == "High":
            d4.warning("P2")
        elif risk_level == "Medium":
            d4.info("P3")
        else:
            d4.success("P4")

        st.divider()
        st.subheader("AI Classification")
        st.info(ai_result)

        st.subheader("Executive Briefing")
        st.warning(executive_summary)
        if risk_level == "Critical":
            priority = "P1"
        elif risk_level == "High":
            priority = "P2"
        elif risk_level == "Medium":
            priority = "P3"
        else:
            priority = "P4"
        st.subheader("Operational Dashboard")
        k1, k2, k3, k4 = st.columns(4)
        if risk_level == "Critical":
            active_incidents = 5
        elif risk_level == "High":
            active_incidents = 3
        elif risk_level == "Medium":
            active_incidents = 2
        else:
            active_incidents = 1
        k1.metric("Active Incidents", active_incidents)
        k2.metric("Risk Level", risk_level)
        k3.metric("Category", category)
        k4.metric("Priority", priority)
        
        st.subheader("Department Impact Analysis")

        if risk_level == "Critical":
            department_data = {
                "Operations": 95,
                "Emergency": 100,
                "Security": 85,
                "ATC": 90,
                "Communications": 80,
                "Maintenance": 70
            }
        elif risk_level == "High":
            department_data = {
                "Operations": 80,
                "Emergency": 60,
                "Security": 85,
                "ATC": 75,
                "Communications": 70,
                "Maintenance": 40
            }
        else:
            department_data = {
                "Operations": 40,
                "Emergency": 20,
                "Security": 30,
                "ATC": 25,
                "Communications": 35,
                "Maintenance": 20
            }

        df = pd.DataFrame(list(department_data.items()), columns=["Department", "Impact"])
        st.bar_chart(df.set_index("Department"))

        fig = px.pie( df,
                     values="Impact",
                     names="Department",
                     title="Department Impact Distribution"
)
        fig.update_traces(
            textposition="inside",
    textinfo="percent+label"
)
        st.subheader("Operational Impact Distribution")
        st.plotly_chart(fig, use_container_width=True)

        if risk_level == "Critical":
            flights, passengers, recovery, priority = "27", "4200", "6 Hours", "P1"
        elif risk_level == "High":
            flights, passengers, recovery, priority = "12", "1800", "3 Hours", "P2"
        elif risk_level == "Medium":
            flights, passengers, recovery, priority = "5", "650", "1 Hour", "P3"
        else:
            flights, passengers, recovery, priority = "0", "0", "Normal", "P4"

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Flights Impacted", flights)
        k2.metric("Passengers Affected", passengers)
        k3.metric("Recovery Time", recovery)
        k4.metric("Priority", priority)

        left, right = st.columns([1, 2])

        with left:
            st.subheader("Incident Summary")
            st.write("Category:", category)
            st.write("Incident:", question)
            st.write("Risk Level:", risk_level)

        with right:
            st.subheader("Affected Departments")
            st.write("\\n".join(department_data.keys()))

        st.subheader("Passenger Communication Draft")

        passenger_message = f"""Dear Passengers,

We are currently managing the following situation:

{question}

Our teams are actively working to minimize disruption and provide updates as they become available.

Thank you for your patience and understanding.

Airport Operations Team"""

        st.text_area("Generated Communication", passenger_message, height=220)

elif page == "Knowledge Base":
    st.subheader("Knowledge Base")
    st.write("""
• Airport Operations Manual
• Crisis Management SOP
• Weather Disruption SOP
• Passenger Communication Policy
• Security Incident Procedures
• Emergency Response Procedures
""")

elif page == "System Status":
    st.subheader("System Status")
    st.success("AI Engine Online")
    st.success("Knowledge Base Connected")
    st.success("Operations Dashboard Active")
