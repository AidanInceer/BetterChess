

def opening_name_cleaner(url):
    """Cleans the opening url to give the opening name."""
    opening_string = url.split("/")[-1]
    clean_opening = str(opening_string.replace("-", " ").strip())
    return clean_opening
