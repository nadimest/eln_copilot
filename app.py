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
    st.markdown(generated_markdown)

    # Copy to Clipboard button
    if st.button('📋 Copy to Clipboard'):
        st.write(f"<script>navigator.clipboard.writeText(`{generated_markdown}`);</script>", unsafe_allow_html=True)

else:
    st.markdown('Markdown output will be shown here...')
