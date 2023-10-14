"""IO utilities."""
import os

from src.text_manipulation_utils import clean_filename_string


def get_string_from_file(folder_path, file_name):
    """
    Read the content of a file as a string.

    Args:
        folder_path (str): The path to the folder containing the file.
        file_name (str): The name of the file to read.

    Returns:
        str: The content of the file as a string.
    """
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "r", encoding="utf8") as file:
        # Write the content to the file
        s = file.read()
    return s


def save_string_to_file(file_name, content, folder_path, format=".md"):
    """
    Save a string as a file with the specified filename and format.

    Args:
        file_name (str): The desired filename for the saved file.
        content (str): The content to be written to the file.
        folder_path (str): The path to the folder where the file will be saved.
        format (str, optional): The file format or extension. Defaults to ".md".

    Returns:
        None
    """
    file_name = clean_filename_string(file_name)
    # Create the full path to the file
    if "." not in file_name:
        file_name = file_name + format
    file_path = os.path.join(folder_path, file_name)
    content = content.encode()
    try:
        # Open the file for writing
        with open(file_path, "wb") as file:
            # Write the content to the file
            file.write(content)
        print(f"File '{file_name}' saved to '{folder_path}'")
    except IOError as e:
        print(f"An error occurred while saving the file: {str(e)}")


def list_files_in_directory(directory_path):
    """
    List all files in a directory and its subdirectories.

    Args:
        directory_path (str): The path to the directory to list files.

    Returns:
        list: A list of file paths in the specified directory and its subdirectories.
    """
    file_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def clean_directory(directory_path):
    """
    Delete all files in a directory and its subdirectories.

    Args:
        directory_path (str): The path to the directory to clean.

    Returns:
        None
    """
    try:
        # Get a list of file paths in the directory
        file_paths = list_files_in_directory(directory_path)

        # Iterate through the file paths and remove each file
        for file_path in file_paths:
            os.remove(file_path)

        print(f"All files in '{directory_path}' have been deleted.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
