import streamlit as st
import os
import json
from components import chat_interface, load_workflows, load_mockup_data

st.set_page_config(layout="wide")

def main():
    st.title('Lab Notebook Copilot')

    # Load workflows
    workflows_data = load_workflows('workflows')
    workflow_options = list(workflows_data.keys())

    # Sidebar for workflow selection
    selected_workflow = st.sidebar.selectbox('Select Workflow', workflow_options)
    instructions = workflows_data.get(selected_workflow, '')

    # Main chat interface
    chat_interface(instructions)

if __name__ == "__main__":
    main()