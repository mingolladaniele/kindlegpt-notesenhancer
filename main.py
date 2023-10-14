"""Process emails and upload book notes to Google Drive."""
import time

from config import check_configuration, config
from src.drive_utils import upload_book_notes_to_drive
from src.email_utils import process_email
from src.google_utils import initialize_google_service


def main():
    """
    Process emails and upload book notes to Google Drive.

    The function checks the configuration, initializes Google services, and continuously
    processes emails using Gmail and uploads book notes to Google Drive. It monitors the
    inbox for new emails matching the provided filter and processes them accordingly.

    Returns:
        None
    """
    # Check configuration before starting
    check_configuration(config)
    gmail_service = initialize_google_service("gmail", "v1")
    drive_service = initialize_google_service("drive", "v3")
    while 1:
        l_books_processed = process_email(
            gmail_service, emails_filter=config.EMAIL_FILTER
        )
        if l_books_processed:
            for book in l_books_processed:
                print(f'Uploading {book["title"]} to drive...')
                upload_book_notes_to_drive(
                    service=drive_service,
                    note_details=book,
                    output_dir_id=config.OUTPUT_DIR_ID,
                )
        else:
            print("No emails to process...")
            time.sleep(10)


if __name__ == "__main__":
    """
    Main function.
    """
    main()
