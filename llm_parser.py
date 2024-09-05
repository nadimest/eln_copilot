import openai

def parse_experiment_instructions(experiment_description, instructions):
    """
    Parse experiment instructions using OpenAI's GPT model.
    
    Args:
    experiment_description (str): Description of the experiment.
    instructions (str): Instructions for the experiment.
    
    Returns:
    str: Parsed output from the LLM.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Generate a detailed output based on the following experiment description and instructions:\n\nExperiment Description: {experiment_description}\n\nInstructions: {instructions}"}
        ]
    )
    return response.choices[0].message['content']

# Add any additional helper functions for LLM parsing here