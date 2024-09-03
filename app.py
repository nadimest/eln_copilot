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

def generate_markdown(selected_workflow, experiment_description):
    selected_preprompt = workflows_data[selected_workflow]
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

    # Copy to Clipboard button with on_click
    st.button('📋 Copy to Clipboard', on_click=copy_to_clipboard, args=(generated_markdown,))

# Clear button
if st.button('Clear'):
    generated_markdown = ""
    st.rerun()
