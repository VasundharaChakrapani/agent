import streamlit as st
import subprocess
import os


st.set_page_config(page_title="AI Issue Triager", layout="wide")

st.title("Autonomous Git-Issue Triager")
st.markdown("AI-powered debugging and static code analysis")


# Sidebar
st.sidebar.header("Configuration")

hf_token = st.sidebar.text_input(
    "Hugging Face Token",
    type="password"
)


# Main Form
st.subheader("Submit GitHub Issue")

issue_title = st.text_input("Issue Title")

issue_description = st.text_area(
    "Issue Description",
    height=200
)


if st.button("Run AI Debugger"):

    # Save token temporarily
    with open(".env", "w") as env_file:
        env_file.write(f"HF_TOKEN={hf_token}")

    st.info("Agent is analyzing repository...")

    # Save issue context
    with open("current_issue.txt", "w", encoding="utf-8") as issue_file:
        issue_file.write(
            f"Issue Title: {issue_title}\n\n"
            f"Issue Description:\n{issue_description}"
        )

    # Run agent
    result = subprocess.run(
        ["venv\\Scripts\\python.exe", "agent_runner.py"],

        capture_output=True,
        text=True
    )

    st.subheader("Agent Console Output")

    st.code(result.stdout)

    report_path = "reports/debug_report.md"

    # Display markdown report
    if os.path.exists(report_path):

        with open(report_path, "r", encoding="utf-8") as file:
            report_content = file.read()

        st.subheader("Debug Report")

        st.markdown(report_content)

        # Download button
        st.download_button(
            label="Download Report",
            data=report_content,
            file_name="debug_report.md",
            mime="text/markdown"
        )

    else:
        st.error("Report generation failed.")