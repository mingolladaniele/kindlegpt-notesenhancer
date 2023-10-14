from email.message import EmailMessage
import re
import base64
from googleapiclient.errors import HttpError
from src.html_utils import extract_book_info
from src.text_manipulation_utils import text_into_template
from src.IO_utils import save_string_to_file, get_string_from_file
from src.chatgpt_utils import gpt_note_processor, num_tokens_from_string
from config import config

# Pattern to extract the sender's email
pattern_ext_email = r"<(.*?)>"


def get_sender_email(service, emails):
    recipient_mail = None
    if len(emails) > 0:
        message = service.users().messages().get(userId="me", id=emails[0]["id"]).execute()
        payload = message["payload"]
        recipient_raw = next(
            (header["value"] for header in payload["headers"] if header["name"] == "From"),
            "",
        )
        recipient_mail = re.search(pattern_ext_email, recipient_raw)
        recipient_mail = recipient_mail.group(1)
    return recipient_mail


def create_email(body, sender, receiver, subject):
    # Create an email message
    message = EmailMessage()

    message["To"] = receiver
    message["From"] = sender
    message["Subject"] = subject

    body = body.encode("utf-8")
    message.add_header("Content-Type", "text/html")
    message.set_payload(body)

    # Encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded_message}
    return create_message


def send_email(service, body, sender, recipient, subject):
    email = create_email(body, sender, recipient, subject)
    # Send the email
    service.users().messages().send(userId="me", body=email).execute()
    print("Email correctly sent!")


def get_attachments(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        parts = [message["payload"]]
        file_data = None
        while parts:
            part = parts.pop()
            if part.get("parts"):
                parts.extend(part["parts"])
            if part.get("filename"):
                if "data" in part["body"]:
                    file_data = base64.urlsafe_b64decode(
                        part["body"]["data"].encode("UTF-8")
                    )
                elif "attachmentId" in part["body"]:
                    attachment = (
                        service.users()
                        .messages()
                        .attachments()
                        .get(
                            userId=user_id,
                            messageId=message["id"],
                            id=part["body"]["attachmentId"],
                        )
                        .execute()
                    )
                    file_data = base64.urlsafe_b64decode(
                        attachment["data"].encode("UTF-8")
                    )
        return file_data
    except HttpError as error:
        print(f"An error occurred: {error}")


def get_book_data_from_email(service, emails):
    book_data_list = []
    for email in emails:
        bytes_obj = get_attachments(service=service, user_id="me", msg_id=email["id"])
        book_title, author, note_text_list = extract_book_info(bytes_obj)
        book_details = {"title": book_title, "author": author, "notes": note_text_list}
        book_data_list.append(book_details)

    return book_data_list


def get_emails(service, emails_filter):
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], q=emails_filter)
        .execute()
    )
    messages = results.get("messages", [])
    # mark the processed messages as read
    for msg in messages:
        service.users().messages().modify(
            userId="me", id=msg["id"], body={"removeLabelIds": ["UNREAD"]}
        ).execute()
    return messages


def process_email(service, emails_filter):
    l_books_processed = []
    l_emails = get_emails(service, emails_filter)
    book_data_list = get_book_data_from_email(service, l_emails)
    sender_notes_email = get_sender_email(service, l_emails)
    # calculate number of tokens of the prompts
    n_token_instructions = num_tokens_from_string(
        get_string_from_file(config.DIR_GPT_PROMPTS, config.DEFAULT_PROMPT)
    )
    # default model
    model_name = "gpt-3.5-turbo-16k"
    for book_date in book_data_list:
        n_token_input = num_tokens_from_string(book_date["notes"])
        total_tokens = n_token_input + n_token_instructions
        if total_tokens <= 8000:
            if total_tokens <= 2000:
                model_name = "gpt-3.5-turbo"
            print(f"Processing {book_date['title']}...")
            book_date["notes"] = gpt_note_processor(
                prompt=book_date["notes"],
                model_name=model_name,
                model_instructions_filename=config.DEFAULT_PROMPT
            )
            final_note = text_into_template(
                template_filename="book_review.txt", template_variables=book_date
            )
            save_string_to_file(
                file_name=book_date["title"],
                content=final_note,
                folder_path=config.INPUT_DIR,
            )
            l_books_processed.append(
                {"title": book_date["title"], "final_note": final_note}
            )
        else:
            print("Number of token exceed! Text not processed!")
            body = f"Number of token exceeds for: {book_date['title']}"
            subject = "Error - Number of tokens exceeds!"
            send_email(service, body, config.SENDER_MAIL, sender_notes_email, subject)
    return l_books_processed
