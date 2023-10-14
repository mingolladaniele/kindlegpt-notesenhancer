"""HTML utilities."""
from bs4 import BeautifulSoup


def extract_title(html_content):
    """
    Extract the title from the HTML content.

    Args:
        html_content (BeautifulSoup): Parsed HTML content.

    Returns:
        str: The title of the book.
    """
    # Extract the title from the HTML content
    return html_content.find("div", class_="bookTitle").text.strip()


def extract_author(html_content):
    """
    Extract the author's name from HTML content.

    Args:
        html_content (BeautifulSoup): Parsed HTML content.

    Returns:
        str: The author's name.
    """
    # Extract the author's name from HTML content
    return html_content.find("div", class_="authors").text.strip()


def extract_notes(html_content):
    """
    Extract notes from HTML content.

    Args:
        html_content (BeautifulSoup): Parsed HTML content.

    Returns:
        str: Combined notes separated by line breaks.
    """
    # Find all elements with the class 'm_noteHeading'
    note_headings = html_content.find_all("div", class_="noteHeading")

    notes = []

    # Iterate through the note headings
    for heading in note_headings:
        # Skip the personal notes to avoid duplicates
        if "Highlight" in heading.text:
            sibling = heading.find_next_sibling("div", class_="noteText")
            text_note = sibling.text.strip()
            sibling_header = sibling.find_next_sibling("div", class_="noteHeading")
            if sibling_header:
                sibling_header_text = sibling_header.text.strip()

                # Check if the following header contains "Note"
                if "Note" in sibling_header_text:
                    personal_note_text = sibling_header.find_next_sibling(
                        "div", class_="noteText"
                    ).text.strip()
                    # Concatenate personal note with the highlight
                    text_note = text_note + f"\n*Personal note*: {personal_note_text}"

            notes.append(text_note)

    # Combine notes into a single string, separated by line breaks
    notes = "\n\n".join(notes)
    return notes


def extract_book_info(file_data):
    """
    Extract book information from HTML content.

    Args:
        file_data (bytes): HTML content as bytes.

    Returns:
        tuple: A tuple containing the book title, author, and note text.
    """
    # Parsing HTML with BeautifulSoup
    html_content = BeautifulSoup(file_data, "html.parser")

    # Extract the title of the book
    book_title = extract_title(html_content)

    # Extract the author
    author = extract_author(html_content)

    # Extract all notes in the attachment
    note_text_list = extract_notes(html_content)

    return book_title, author, note_text_list
