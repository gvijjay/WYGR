import streamlit as st
from wygr.agents.medical_agent import Cardiologist,Psychologist,Pulmonologist,MultidisciplinaryTeam
from dotenv import load_dotenv

load_dotenv()

st.title("AI Medical Diagnosis System 🏥")

# Upload or paste the medical report
uploaded_file = st.file_uploader("Upload Patient's Medical Report (.txt)", type=["txt"])


# Specialist selection
specialist = st.selectbox("Select the Specialist", ["Cardiologist", "Psychologist", "Pulmonologist"])

if st.button("Run AI Diagnosis"):
    medical_report = uploaded_file.read().decode("utf-8")

    if not medical_report:
        st.warning("Please provide a medical report.")
    else:
        st.info(f"Sending report to {specialist} for diagnosis...")

        # Select the right AI agent
        if specialist == "Cardiologist":
            agent = Cardiologist(medical_report)
        elif specialist == "Psychologist":
            agent = Psychologist(medical_report)
        elif specialist == "Pulmonologist":
            agent = Pulmonologist(medical_report)

        diagnosis = agent.run()

        # Display result
        st.subheader(f"🏥 {specialist}'s Diagnosis")
        st.success(diagnosis)

        # Save the report
        report_content = f"""Medical Diagnosis Report
===========================
Specialist: {specialist}

Diagnosis:
{diagnosis}
"""
        with open("results/diagnosis.txt", "w") as file:
            file.write(report_content)

        st.download_button("📥 Download Report", report_content, "diagnosis.txt")
