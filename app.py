import streamlit as st
import json
import pyperclip
import time

st.title('Biotech Data Collector App')

# Load workflows from JSON file
with open('workflows.json', 'r') as f:
    workflows_data = json.load(f)

# Extract workflow names for dropdown
workflow_options = [workflow['name'] for workflow in workflows_data['workflows']]

# Input box for experiment description
experiment_description = st.text_area('Experiment Description', 'Enter the experiment details here...')

# Dropdown to select a workflow
selected_workflow = st.selectbox('Select Workflow', workflow_options)

# Initialize a variable to hold generated markdown
generated_markdown = ""

def generate_markdown(selected_workflow, experiment_description):
    selected_preprompt = next(workflow['preprompt'] for workflow in workflows_data['workflows'] if workflow['name'] == selected_workflow)
    return f'''### {selected_workflow} Markdown

**Preprompt:** {selected_preprompt}

**Experiment Description:**
{experiment_description}'''

def copy_to_clipboard(markdown):
    pyperclip.copy(markdown)
    st.success("Copied to clipboard!", icon="✅")
    time.sleep(1)  # Wait for 1 second
    st.empty()  # Clear the success message

# Generate button
if st.button('Generate Markdown'):
    generated_markdown = generate_markdown(selected_workflow, experiment_description)

# Output box to render markdown
if generated_markdown:
    st.code(generated_markdown, language="wiki")

    # Copy to Clipboard button
    if st.button('📋 Copy to Clipboard'):
        copy_to_clipboard(generated_markdown)

# Clear button
if st.button('Clear'):
    generated_markdown = ""
    st.experimental_rerun()
