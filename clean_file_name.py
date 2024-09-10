import os
import re
from urllib.parse import urlparse


def make_cleaned_filename(text, replacement='_'):
    # Remove characters not allowed in Windows file names
    cleaned_text = re.sub(r'[<>:"/\\|?*]', replacement, text)

    # Remove leading and trailing spaces and dots
    cleaned_text = cleaned_text.strip().strip('.')

    # Ensure the filename is not empty after cleaning
    if not cleaned_text:
        cleaned_text = 'unnamed_file'

    # Ensure the filename does not exceed 255 characters (Windows limit)
    cleaned_text = cleaned_text[:255]

    return cleaned_text


# Example usage
url = 'https://static.bhphoto.com/images/itemImgPlaceholder.jpg'
