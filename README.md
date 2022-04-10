# Overview

- This is a project for chess which analysis a users chess.com games

## To do

### Python

1. Fix bottlenecks / speed up processing

    - Look into multi processing
    - Look into numpy arrays for elements instead of list
    - allocate more cpu to stockfish?

2. Implement optional variable to determine "deep" or "shallow" analysis.
3. Link usernames up properly to file names (allows separate storage of analysis)
4. doc strings
5. Simplify the "get_user_data" main function -> export to separate functions
6. remove redundant functions


### Web App (javascript, html, css, flask)

1. look into building a simple web app
2. how to interact with the data pull out for a user on the web app?
3. building the chess features in the app
4. layout and interactions of the app

### Database interation

1. store database im a mySQL database
2. how to pull data from the database to the webapp

### Insights/PowerBI export

1. query data so it can be used in "insight"
2. export to a powerBI dashboard - vary for each user?
