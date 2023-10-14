"""Google authentication utilities."""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import config


def initialize_google_service(api_name, api_version):
    """
    Initialize and authenticate with a Google API service.

    Args:
        api_name (str): The name of the Google API (e.g., "gmail", "drive").
        api_version (str): The version of the API to use.

    Returns:
        googleapiclient.discovery.Resource: The authenticated Google API service.
    """
    creds = None
    credentials_filename = config.CREDENTIALS_FILENAME
    token_filename = config.TOKEN_FILENAME
    scopes = config.SCOPES
    auth_dir = config.AUTH_DIR
    token_path = os.path.join(auth_dir, token_filename)

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials = os.path.join(auth_dir, credentials_filename)
            flow = InstalledAppFlow.from_client_secrets_file(credentials, scopes)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    service = build(api_name, api_version, credentials=creds)
    return service
