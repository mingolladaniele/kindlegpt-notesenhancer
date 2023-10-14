"""Google Drive utilities."""
import io
import os

from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

from src.IO_utils import list_files_in_directory


def upload_book_notes_to_drive(service, note_details, output_dir_id):
    """
    Upload a book note to Google Drive.

    Args:
        service: The Google Drive service.
        note_details (dict): Details of the book note, including "title" and "final_note".
        output_dir_id (str): The ID of the output directory on Google Drive.

    Returns:
        None
    """
    file_meta = {"name": note_details["title"] + ".md", "parents": [output_dir_id]}
    f = io.BytesIO(note_details["final_note"].encode())
    media_content = MediaIoBaseUpload(f, mimetype="text/plain")
    # upload the file
    service.files().create(body=file_meta, media_body=media_content).execute()
    # release the uploaded file to be removed later
    media_content = None
    out_dir_name = (
        service.files().get(fileId=output_dir_id, fields="name").execute()["name"]
    )
    print(f"{file_meta['name']} uploaded in the folder {out_dir_name} on GDrive!")


def upload_to_drive(service, input_dir, output_dir_id):
    """
    Upload files from a local directory to Google Drive.

    Args:
        service: The Google Drive service.
        input_dir (str): The local directory containing files to upload.
        output_dir_id (str): The ID of the output directory on Google Drive.

    Returns:
        None
    """
    l_filepath = list_files_in_directory(input_dir)
    for filepath in l_filepath:
        filename = os.path.basename(filepath)
        file_meta = {"name": filename, "parents": [output_dir_id]}
        media_content = MediaFileUpload(filepath)
        # upload the file
        service.files().create(body=file_meta, media_body=media_content).execute()
        # release the uploaded file to be removed later
        media_content = None
        out_dir_name = (
            service.files().get(fileId=output_dir_id, fields="name").execute()["name"]
        )
        print(f"{filename} uploaded in the folder {out_dir_name} on GDrive!")
    # clean_directory(input_dir)
