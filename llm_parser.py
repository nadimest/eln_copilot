from openai import OpenAI
from models import  ExperimentOutput

client = OpenAI()

def parse_experiment_instructions(messages: list, instructions: str):
    """
    Parse experiment instructions using OpenAI's GPT model with streaming.
    
    Args:
    messages (list): List of previous messages in the conversation.
    instructions (str): Instructions for the experiment.
    
    Returns:
    A stream object that can be used with st.write_stream
    """
    full_messages = [
        {"role": "system", "content": instructions},
        *messages
    ]
    
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=full_messages,
        stream=True,
    )



def parse_description_to_table(instructions):
    """
    Parse the LLM output into a structured ExperimentOutput using a response model.
    
    Args:
    llm_output (str): The output from the first LLM call.
    
    Returns:
    ExperimentOutput: A structured output containing samples and heatmap configuration.
    """

    prompt = f"""Parse the following experiment description into a structured output containing a list of Sample instances and
      a HeatmapConfig.  For the Metadata attribute, parse the Sample Instance using the sample name as key and the remainder attributes as values.   
      Respond with valid JSON that matches the ExperimentOutput model: \n\n {instructions}"""
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that parses experiment descriptions into structured data."},
            {"role": "user", "content": prompt}
        ],
        response_format=ExperimentOutput
    )
    
    structured_output = response.choices[0].message.parsed
    return structured_output


# Add any additional helper functions for LLM parsing here


import pydantic


def main():

    response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that parses experiment descriptions into structured data."},
        {"role": "user", "content": f"Parse the following experiment description into a structured output containing a list of Sample instances and a HeatmapConfig. Respond with valid JSON that matches the ExperimentOutput model:\n\n{instructions}"}
    ],
    response_format=ExperimentOutput
)

    structured_output = response.choices[0].message.parsed
    return 

if __name__ == '__main__':
    main()


