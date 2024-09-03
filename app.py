import streamlit as st
import os
import pyperclip
import time
import openai
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd

# Set OpenAI API key from environment variable
openai.api_key = st.secrets['open_ai_key']

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

# Sidebar for input box and workflow selection
st.sidebar.header("Input Section")
experiment_description = st.sidebar.text_area('Experiment Description', 'Enter the experiment details here...')
selected_workflow = st.sidebar.selectbox('Workflows', workflow_options)  # Updated label

def copy_to_clipboard():
    if 'output_buffer' in st.session_state:
        pyperclip.copy(st.session_state.output_buffer)
        st.success("Copied to clipboard!", icon="✅")
        time.sleep(1)  # Wait for 1 second

def generate_output(experiment_description, instructions):
    # Call to OpenAI GPT-4o-mini with streaming
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Generate a detailed output based on the following experiment description and instructions:\n\nExperiment Description: {experiment_description}\n\nInstructions: {instructions}"}
        ],
        stream=True  # Enable streaming
    )
    
    return response

def clear_output():
    st.session_state.output_buffer = ""
    st.session_state.output_placeholder.markdown("")  # Clear the output display

def handle_generate_output():
    instructions = workflows_data.get(selected_workflow, '')
    
    # Clear the output buffer before generating new output
    clear_output()
    # Create a placeholder for the output
    output_placeholder = st.session_state.output_placeholder

    with st.chat_message("assistant"):
        with st.spinner("Generating output..."):  # Show loading spinner
            stream = generate_output(experiment_description, instructions)
            for chunk in stream:
                content = chunk['choices'][0]['delta'].get('content', '')
                st.session_state.output_buffer += content  # Append the new content to the buffer
                output_placeholder.markdown(st.session_state.output_buffer)  # Update the output display

    # Generate and display the Plotly chart
    display_plotly_chart()

def display_plotly_chart():
    # Sample data for the plate layout
    data = {
        'Sample': ['Sample 1', 'Sample 2', 'Sample 3', 'Sample 4'],
        'Row': ['A', 'A', 'B', 'B'],
        'Column': ['1', '2', '1', '2'],
        'Value': [1, 2, 3, 4]  # Example values for the heatmap
    }
    
    df = pd.DataFrame(data)

    # Create a heatmap using Plotly
    heatmap_data = df.pivot(index="Row", columns="Column", values="Value")
    fig = ff.create_annotated_heatmap(z=heatmap_data.values, 
                                       x=heatmap_data.columns.tolist(), 
                                       y=heatmap_data.index.tolist(),
                                       colorscale='Viridis', 
                                       showscale=True)

    # Update layout for better visualization
    fig.update_layout(title="Sample Plate Layout Heatmap", 
                      xaxis_title="Columns", 
                      yaxis_title="Rows")

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

# Expandable section to show workflow instructions
if selected_workflow:
    with st.expander("Instructions", expanded=False):  # Updated label
        st.markdown(workflows_data[selected_workflow])

# Output section
if 'output_buffer' not in st.session_state:
    st.session_state.output_buffer = ""  # Initialize output_buffer in session state
if 'output_placeholder' not in st.session_state:
    st.session_state.output_placeholder = st.empty()  # Initialize output placeholder in session state

# Generate Output button
st.button('Generate Output', on_click=handle_generate_output)  # Use on_click with the new function

# Output display
st.header("Output Section")  # Added header for output section
st.markdown(st.session_state.output_buffer)  # Display the output buffer

# Copy to Clipboard button
st.button('📋 Copy to Clipboard', on_click=copy_to_clipboard)  # Use on_click without args
