import streamlit as st
import os
import json
import pandas as pd
from models import Sample, HeatmapConfig, ExperimentOutput
from heatmap_visualizer import create_heatmap
from llm_parser import parse_experiment_instructions, parse_description_to_table
import pyperclip

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
        return None, None

def display_experiment_output(experiment_output):
    if experiment_output is None:
        st.warning("No structured output available for this response.")
        return

    st.subheader("Experiment Output")
    st.write(f"Plate Size: {experiment_output.plate_size}")
    st.write(f"Rows: {', '.join(experiment_output.rows)}")
    st.write(f"Columns: {', '.join(experiment_output.columns)}")
    
    st.subheader("Samples")
    df = pd.DataFrame([s.model_dump() for s in experiment_output.samples])
    st.dataframe(df)

    st.subheader("Sample Grid Visualization")
    metadata_options = [field for field in experiment_output.samples[0].model_dump().keys() if field not in ['sample_name', 'position']]
    
    # Select all metadata options by default
    selected_metadata = st.multiselect(
        "Select metadata to display",
        options=metadata_options,
        default=metadata_options 
    )
    
    if selected_metadata:
        for metadata in selected_metadata:
            try:
                fig = create_heatmap(experiment_output.samples, experiment_output, metadata)
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error creating sample grid for {metadata}: {str(e)}")
    else:
        st.warning("Please select at least one metadata option to display.")

def show_workflow_modal(workflow_content):
    st.session_state.show_modal = True
    st.session_state.modal_content = workflow_content

def hide_workflow_modal():
    st.session_state.show_modal = False

def sidebar_inputs(initial_workflows):
    if "workflows" not in st.session_state:
        st.session_state.workflows = initial_workflows

    if "editing_workflow" not in st.session_state:
        st.session_state.editing_workflow = False

    st.sidebar.header("Settings")
    
    # Toggle for structured data generation
    if "generate_structured_data" not in st.session_state:
        st.session_state.generate_structured_data = True
    
    st.session_state.generate_structured_data = st.sidebar.toggle(
        "Generate Structured Data",
        value=st.session_state.generate_structured_data
    )

    st.sidebar.header("Workflow Selection")
    selected_workflow = st.sidebar.selectbox('Workflow', list(st.session_state.workflows.keys()))

    # Show workflow content in sidebar expander
    with st.sidebar.expander("View/Edit Selected Workflow", expanded=True):
        if not st.session_state.editing_workflow:
            st.markdown(st.session_state.workflows[selected_workflow])
            if st.button("Edit"):
                st.session_state.editing_workflow = True
                st.rerun()
        else:
            edited_content = st.text_area(
                "Workflow Content",
                value=st.session_state.workflows[selected_workflow],
                height=300
            )
            if st.button("Save Changes"):
                st.session_state.workflows[selected_workflow] = edited_content
                st.session_state.editing_workflow = False
                st.success("Workflow content updated!")
                st.rerun()
    
    return selected_workflow


def chat_interface(instructions):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "current_structured_output" not in st.session_state:
        st.session_state.current_structured_output = None

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Chat input
    if prompt := st.chat_input("What would you like to know about the experiment?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate LLM response
        with st.chat_message("assistant"):
            stream = parse_experiment_instructions(st.session_state.messages, instructions)
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Generate structured output with spinner
        if st.session_state.generate_structured_data:
            with st.spinner("Generating structured output..."):
                try:
                    structured_output = parse_description_to_table(response)
                    st.session_state.current_structured_output = structured_output
                    st.success("Structured output generated successfully!")
                except Exception as e:
                    st.error(f"Error generating structured output: {str(e)}")
                    st.session_state.current_structured_output = None

    # Display structured output expander if available
    if st.session_state.generate_structured_data and st.session_state.current_structured_output is not None:
        with st.expander("View Structured Output", expanded=True):
            display_experiment_output(st.session_state.current_structured_output)

        st.button(
            "Copy Output",
            on_click=copy_to_clipboard,
            key="copy_button"
        )

def copy_to_clipboard():
    if st.session_state.messages:
        last_message = st.session_state.messages[-1]["content"]
        pyperclip.copy(last_message)
        st.success('Last message copied to clipboard!')