# Authentication
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILENAME = "credentials.json"
TOKEN_FILENAME = "token.json"
AUTH_DIR = "./auth/"

# Email settings
SENDER_MAIL = "XXX"

# Drive
INPUT_DIR = "./data/files_to_upload/"

# Template
DIR_GPT_PROMPTS = "./data/prompts/"
DEFAULT_PROMPT = "notes_cleaner.txt"