import streamlit as st
import os
import pyperclip
import time

st.title('Biotech Data Collector App')

# Load workflows from markdown files in the workflows folder
workflows_data = {}
workflows_folder = 'workflows'
for filename in os.listdir(workflows_folder):
    if filename.endswith('.md'):
        with open(os.path.join(workflows_folder, filename), 'r') as f:
            workflows_data[filename[:-3]] = f.read()  # Store the content without the .md extension

# Extract workflow names for dropdown
workflow_options = list(workflows_data.keys())

# Input box for experiment description
experiment_description = st.text_area('Experiment Description', 'Enter the experiment details here...')

# Dropdown to select a workflow
selected_workflow = st.selectbox('Select Workflow', workflow_options)

# Initialize a variable to hold generated markdown
generated_markdown = ""

def copy_to_clipboard(markdown):
    pyperclip.copy(markdown)
    st.success("Copied to clipboard!", icon="✅")
    time.sleep(1)  # Wait for 1 second
    st.empty()  # Clear the success message

# Expandable section to show workflow instructions
if selected_workflow:
    with st.expander("Workflow Instructions", expanded=True):
        st.markdown(workflows_data[selected_workflow])

# Output box to render experiment description
if experiment_description:
    st.markdown(f"**Experiment Description:** {experiment_description}")

# Copy to Clipboard button
if st.button('📋 Copy to Clipboard'):
    copy_to_clipboard(experiment_description)

# Clear button
if st.button('Clear'):
    st.rerun()
