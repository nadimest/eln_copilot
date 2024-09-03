import streamlit as st
import json

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

# Generate button
if st.button('Generate Markdown'):
    # Find the selected workflow's preprompt
    selected_preprompt = next(workflow['preprompt'] for workflow in workflows_data['workflows'] if workflow['name'] == selected_workflow)
    
    # Generate markdown using the preprompt
    generated_markdown = f'''### {selected_workflow} Markdown

**Preprompt:** {selected_preprompt}

**Experiment Description:**
{experiment_description}'''

# Output box to render markdown
if generated_markdown:
    st.markdown(generated_markdown)

# Clear button
if st.button('Clear'):
    generated_markdown = ""
    st.experimental_rerun()
