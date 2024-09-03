import streamlit as st
import os
import pyperclip
import time
import openai
import plotly.figure_factory as ff
import pandas as pd
from models import HeatmapConfig  # Import the HeatmapConfig model

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

# Fixed heatmap configuration
fixed_heatmap_config = HeatmapConfig(
    plate_size=96,
    rows=["A", "B", "C", "D", "E", "F", "G", "H"],
    columns=["1", "2", "3", "4", "5", "6", "7", "8"],
    metadata={"Sample 1": {"description": "Control sample", "concentration": 5.0}}
)

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

    # Automatically generate and display the Plotly chart
    display_plotly_chart(fixed_heatmap_config)

def display_plotly_chart(heatmap_config: HeatmapConfig):
    # Create a DataFrame based on the heatmap configuration
    data = {
        'Sample': [f"Sample {i+1}" for i in range(heatmap_config.plate_size)],
        'Row': [heatmap_config.rows[i // len(heatmap_config.columns) % len(heatmap_config.rows)] for i in range(heatmap_config.plate_size)],
        'Column': [heatmap_config.columns[i % len(heatmap_config.columns)] for i in range(heatmap_config.plate_size)],
        'Value': [i + 1 for i in range(heatmap_config.plate_size)]  # Example values for the heatmap
    }
    
    df = pd.DataFrame(data)

    # Create a heatmap using Plotly
    heatmap_data = df.pivot(index="Row", columns="Column", values="Value")
    fig = ff.create_annotated_heatmap(z=heatmap_data.values, 
                                       x=heatmap_data.columns.tolist(), 
                                       y=heatmap_data.index.tolist(),
                                       colorscale='Viridis', 
                                       showscale=True)

    # Reverse the Y-axis
    fig.update_yaxes(autorange="reversed")

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
