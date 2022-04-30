

def opening_name_cleaner(url):
    """Cleans the opening url to give the opening name."""
    opening_string = url.split("/")[-1]
    clean_opening = str(opening_string.replace("-", " ").strip())
    return clean_opening


def termination_filter(termination_raw, username):
    winner_check = termination_raw.split(" ")
    end_string = str(" ".join(winner_check[2:]))
    if winner_check[0] != username:
        termination = username + " lost " + end_string
    else:
        termination = termination_raw
    return termination
