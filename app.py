import streamlit as st
import os
import pyperclip
import time
import openai

st.title('Lab Notebook Copilot')  # Updated app title

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
selected_workflow = st.selectbox('Workflows', workflow_options)  # Updated label

# Initialize a variable to hold generated markdown
output_text = ""

def copy_to_clipboard(markdown):
    pyperclip.copy(markdown)
    st.success("Copied to clipboard!", icon="✅")
    time.sleep(1)  # Wait for 1 second
    st.empty()  # Clear the success message

def generate_output(experiment_description, instructions):
    # Call to OpenAI GPT-4o-mini
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Generate a detailed output based on the following experiment description and instructions:\n\nExperiment Description: {experiment_description}\n\nInstructions: {instructions}"}
        ]
    )
    return response['choices'][0]['message']['content']

# Expandable section to show workflow instructions
if selected_workflow:
    with st.expander("Instructions", expanded=False):  # Updated label
        st.markdown(workflows_data[selected_workflow])

# Output section
if st.button('Generate Output'):  # New button to generate output
    instructions = workflows_data.get(selected_workflow, '')
    output_text = generate_output(experiment_description, instructions)

# Display the output text only once
if output_text:
    st.markdown(output_text)

# Copy to Clipboard button
if st.button('📋 Copy to Clipboard'):
    copy_to_clipboard(output_text)

# Clear button
if st.button('Clear'):
    st.rerun()
