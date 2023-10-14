import os
import openai
from config import config
import tiktoken


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def gpt_note_processor(prompt, model_name, model_instructions_filename="notes_cleaner.txt"):
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
