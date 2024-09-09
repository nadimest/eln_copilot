import streamlit as st
import os
import json
from components import chat_interface, load_workflows, sidebar_inputs

# Set page config
st.set_page_config(
    page_title="Lab Notebook Copilot",  # This will be the name in the browser tab
    page_icon="🧪",  # You can also set a custom icon here
    layout="wide",  # This is optional, adjust as needed
    initial_sidebar_state="expanded"  # This is optional, adjust as needed
)

def main():
    st.title('Lab Notebook Copilot')

    # Load workflows
    workflows_data = load_workflows('workflows')
    
    # Sidebar for workflow selection
    selected_workflow = sidebar_inputs(workflows_data)
    instructions = workflows_data.get(selected_workflow, '')

    # Main chat interface
    chat_interface(instructions)

if __name__ == "__main__":
    main()