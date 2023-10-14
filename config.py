"""This module defines configuration settings for your program."""

from collections import namedtuple

# Define a named tuple for configuration
Config = namedtuple(
    "Config",
    [
        "SCOPES",
        "CREDENTIALS_FILENAME",
        "TOKEN_FILENAME",
        "AUTH_DIR",
        "SENDER_MAIL",
        "EMAIL_FILTER",
        "INPUT_DIR",
        "OUTPUT_DIR_ID",
        "OPENAI_API_KEY",
        "DIR_GPT_PROMPTS",
        "DEFAULT_PROMPT",
        "DEFAULT_TEMPLATE",
    ],
)

# Configuration values
config = Config(
    # Google authentication - DON'T TOUCH
    SCOPES=[
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/drive",
    ],
    CREDENTIALS_FILENAME="credentials.json",
    TOKEN_FILENAME="token.json",
    AUTH_DIR="./auth/",
    # Email settings
    SENDER_MAIL="",
    EMAIL_FILTER="is:unread has:attachment filename:html",
    # Google Drive settings
    INPUT_DIR="./data/files_to_upload/",
    OUTPUT_DIR_ID="",
    # ChatGPT settings
    OPENAI_API_KEY="",
    DIR_GPT_PROMPTS="./data/prompts/",
    DEFAULT_PROMPT="notes_cleaner.txt",
    DEFAULT_TEMPLATE="book_review.txt",
)


def check_configuration(config):
    """
    Check the provided configuration for missing or empty fields.

    Args:
        config (namedtuple): The configuration to be checked.

    Raises:
        ValueError: If any configuration field is missing or empty.

    """
    for field in config._fields:
        if not getattr(config, field, None):
            raise ValueError(f"Configuration field '{field}' is missing or empty.")
