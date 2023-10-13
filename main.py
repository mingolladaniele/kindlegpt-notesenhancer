from src.google_utils import initialize_google_service
from src.email_utils import process_email
from src.drive_utils import upload_book_notes_to_drive
import time
import config


def main():
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
    main()
