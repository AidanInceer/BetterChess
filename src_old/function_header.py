

def opening_clean(url):
    """Cleans the opening url to give the opening name."""
    opening_string = url.split("/")[-1]
    clean_opening = str(opening_string.replace("-", " ").strip())
    return clean_opening


def termination_clean(termination_raw, username):
    """Cleans the termination statement to be based around the user."""
    winner_check = termination_raw.split(" ")
    draw_check = " ".join(winner_check[0:2])
    if winner_check[0] == username:
        termination = "Win " + " ".join(winner_check[2:])
    elif draw_check == "Game drawn":
        termination = "Draw " + " ".join(winner_check[2:])
    else:
        termination = "Loss " + " ".join(winner_check[2:])
    return termination
