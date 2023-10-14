"""Text manipulation utilities."""

import datetime
import os
import re


def clean_filename_string(i_string):
    """
    Clean a string to remove special characters that are not safe for filenames.

    Args:
        i_string (str): The input string to be cleaned.

    Returns:
        str: The cleaned string with special characters removed or replaced.
    """
    symbols_to_remove = [
        "#",
        "%",
        "&",
        "{",
        "}",
        "\\",
        "<",
        ">",
        "*",
        "?",
        "/",
        " ",
        "$",
        "!",
        "'",
        '"',
        ":",
        "@",
        "+",
        "`",
        "|",
        "=",
    ]
    # Escape special characters in the symbols and join them with '|'
    pattern = r"[" + re.escape("".join(symbols_to_remove)) + "]"
    # Use re.sub to replace the matched symbols with an empty string
    result = re.sub(pattern, " ", i_string)
    return result


def text_into_template(template_filename, template_variables):
    """
    Generate a text document from a template file by replacing placeholders.

    Args:
        template_filename (str): The filename of the template file.
        template_variables (dict): A dictionary of variables to replace in the template.

    Returns:
        str: The text document with placeholders replaced by their values.
    """
    template_folder = "./assets/note_templates/"
    template_path = os.path.join(template_folder, template_filename)

    try:
        # Open the file for reading
        with open(template_path, "r", encoding="utf8") as file:
            file_contents = file.read()

        # Get the current date
        current_date = datetime.date.today()

        # Format the date as "YYYY-MM-DD"
        formatted_date = current_date.strftime("%Y-%m-%d")
        template_variables["date"] = formatted_date

        # Replace placeholders with their corresponding values
        replaced_contents = file_contents.format(**template_variables)

        return replaced_contents

    except FileNotFoundError:
        print(f"File not found: {template_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
