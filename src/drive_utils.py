from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from src.IO_utils import list_files_in_directory, clean_directory
import os
import io


def upload_book_notes_to_drive(service, note_details, output_dir_id):
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
