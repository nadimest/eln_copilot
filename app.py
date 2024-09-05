import streamlit as st
import os
import json
from models import Sample, HeatmapConfig
from components import sidebar_inputs, llm_parsing_section, sample_grid_visualization, display_raw_data

def load_workflows(folder):
    workflows_data = {}
    for filename in os.listdir(folder):
        if filename.endswith('.md'):
            with open(os.path.join(folder, filename), 'r') as f:
                workflows_data[filename[:-3]] = f.read()
    return workflows_data

def load_mockup_data(file_path):
    try:
        with open(file_path, "r") as f:
            mockup_data = json.load(f)
        samples = [Sample(**sample) for sample in mockup_data["samples"]]
        heatmap_config = HeatmapConfig(**mockup_data["heatmap_config"])
        return samples, heatmap_config
    except Exception as e:
        st.error(f"Error loading mockup data: {str(e)}")
        return [], None

def main():
    st.set_page_config(page_title="Lab Notebook Copilot", layout="wide")
    st.title('Lab Notebook Copilot')

    # Load workflows
    workflows_data = load_workflows('workflows')
    workflow_options = list(workflows_data.keys())

    # Sidebar inputs
    experiment_description, selected_workflow = sidebar_inputs(workflow_options)

    # Load mockup data
    samples, heatmap_config = load_mockup_data("mockup_data.json")

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        llm_parsing_section(experiment_description, workflows_data.get(selected_workflow, ''))

    with col2:
        sample_grid_visualization(samples, heatmap_config)

    # Raw data display
    display_raw_data(samples, heatmap_config)

if __name__ == "__main__":
    main()
