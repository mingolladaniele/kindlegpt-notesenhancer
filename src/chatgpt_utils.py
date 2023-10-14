"""ChatGPT utilities."""
import os

import openai
import tiktoken

from config import config


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """
    Calculate the number of tokens in the given string.

    Args:
        string (str): The input text string.
        encoding_name (str): The name of the token encoding to use (default is "cl100k_base").

    Returns:
        int: The number of tokens in the input string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def gpt_note_processor(
    prompt, model_name, model_instructions_filename="notes_cleaner.txt"
):
    """
    Generate a response from the ChatGPT model based on the provided prompt.

    Args:
        prompt (str): The user's input prompt.
        model_name (str): The name of the ChatGPT model to use.
        model_instructions_filename (str): The filename of model instructions (default is "notes_cleaner.txt").

    Returns:
        str: The generated response from the ChatGPT model.
    """
    openai.api_key = config.OPENAI_API_KEY

    # Read the model instructions
    model_instructions_filepath = os.path.join(
        config.DIR_GPT_PROMPTS, model_instructions_filename
    )
    with open(model_instructions_filepath, "r") as f:
        model_instructions = f.read()

    completion = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "user", "content": f"{model_instructions}\n\n Text: {prompt}"}
        ],
        temperature=0.2,
    )
    answer = completion["choices"][0]["message"]["content"].strip()
    return answer
