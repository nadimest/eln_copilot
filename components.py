import streamlit as st
import pandas as pd
from models import Sample, HeatmapConfig
from heatmap_visualizer import create_heatmap

def sidebar_inputs(workflow_options):
    st.sidebar.header("Input Section")
    selected_workflow = st.sidebar.selectbox('Workflows', workflow_options)
    experiment_description = st.sidebar.text_area('Experiment Description', 'Enter the experiment details here...')
    return experiment_description, selected_workflow

def llm_parsing_section(experiment_description, instructions):
    st.header("LLM Parsing Output")
    if st.button('Generate Output'):
        with st.spinner("Generating output..."):
            try:
                from llm_parser import parse_experiment_instructions
                llm_output = parse_experiment_instructions(experiment_description, instructions)
                st.write(llm_output)
            except Exception as e:
                st.error(f"Error generating output: {str(e)}")

def sample_grid_visualization(samples, heatmap_config):
    st.header("Sample Grid Visualization")
    if samples and heatmap_config:
        sample_dict = samples[0].model_dump()
        metadata_options = [field for field in sample_dict.keys() if field not in ['sample_name', 'position']]
        
        selected_metadata = st.multiselect("Select metadata to display", metadata_options)
        
        if selected_metadata:
            for metadata in selected_metadata:
                try:
                    fig = create_heatmap(samples, heatmap_config, metadata)
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"Error creating sample grid for {metadata}: {str(e)}")
        else:
            st.warning("Please select at least one metadata option to display.")
    else:
        st.warning("No sample data or heatmap configuration available.")

def display_raw_data(samples, heatmap_config):
    if st.checkbox("Show raw data"):
        st.subheader("Sample Data")
        if samples:
            st.write(pd.DataFrame([s.model_dump() for s in samples]))
        else:
            st.warning("No sample data available.")
        
        st.subheader("Heatmap Configuration")
        if heatmap_config:
            st.json(heatmap_config.model_dump())
        else:
            st.warning("No heatmap configuration available.")