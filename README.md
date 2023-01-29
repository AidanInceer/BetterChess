# Better Chess

![coverage](https://github.com/AidanInceer/BetterChess/blob/master/coverage.svg)
[![lint](https://github.com/AidanInceer/BetterChess/actions/workflows/lint.yml/badge.svg)](https://github.com/AidanInceer/BetterChess/actions/workflows/lint.yml)
[![test](https://github.com/AidanInceer/BetterChess/actions/workflows/test.yml/badge.svg)](https://github.com/AidanInceer/BetterChess/actions/workflows/test.yml)
[![scan](https://github.com/AidanInceer/BetterChess/actions/workflows/scan.yml/badge.svg)](https://github.com/AidanInceer/BetterChess/actions/workflows/scan.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=AidanInceer_BetterChess&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=AidanInceer_BetterChess)
[![build](https://github.com/AidanInceer/BetterChess/actions/workflows/build.yml/badge.svg)](https://github.com/AidanInceer/BetterChess/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a project which enables a user to peform bulk analysis on their **chess.com** games for free,
pull out insights and eventually have access to an interactive webapp to help them develop further.

## Installation & Setup

Currently only works with `python 3.9`. Download the repository and follow the steps below:

``` sh
python -m venv venv
```

``` sh
venv/scripts/activate
```

``` sh
pip install requirements.txt
```

Add a `.env` you the root of your project. This will be used to add your database type, information and stockfish filepaths.

Stockfish will need to be downloaded from: (https://stockfishchess.org/download/) and added to your `./lib/` folder, the version may vary and therefore you need to add the folder name and file name to your `.env` - see below.

If using an external database you will have to configure and set this up - then add these variables into the `.env` file.

```conf
# Select database type from the following options ('mysql', 'sqlite')
# to be implemented: csv, postgresql, cloud (aws, azure)
DB_TYPE = ...


# Fill in if using mysql database. 
mysql_driver = ...
mysql_user = ...
mysql_password = ...
mysql_host = ...
mysql_db = ...

# Fill in stockfish file and details
stockfish_folder = ...
stockfish_exe_file = ...

```


## Running

Running `main.py` will give two options: `manage` and `run`. Firstly `manage` will allow you to quickly get information about the database - see below for the following options:

```txt
reset - Reset the database and cleans down all the log files.
size - the size of the tables.
head - View the head of the tables.
pass - cancel
```

The second option, `run`, will allow you to analyse a given users game data. You will need to enter a chess.com username, engine depth, analysis start year & month.
e.g.
(https://github.com/AidanInceer/BetterChess/blob/master/imgs/examples/run.png)



## Authors

Aidan Inceer