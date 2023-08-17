# NBA Hoops Hunch Game


### Video Demo:  <https://youtu.be/U6AUmP2Unyw>


### Intro
Welcome to the **NBA Hoops Hunch** game! Test your NBA knowledge by filling in a grid 
with players who have played on both teams shown. Use your skills and insights
to find matching players. One goal: complete the grid!

Inspired by: <https://www.hoopgrids.com/>


## Table of Contents
- [Description](#description)
- [Dependencies](#dependencies)
- [How to Play](#how-to-play)
- [Files and functions](#files-and-functions)


## Description
This Python script implements the **"NBA Hoops Hunch"** game. The game comes with a 3x3 
grid with NBA teams in the row and column headers. Your goal is to guess players who 
have played for both teams specified by their numeric positions in the grid.

The game uses the **NBA API** to fetch information about teams and players. There are
interactive features, such as terminal-based play and a nice colorful formatting.


## Dependencies
- `nba_api`
- `numpy`
- `os`
- `pandas`
- `pyfiglet`
- `random`
- `re`
- `sys`
- `tabulate`
- `termcolor`
- `time`
- `typing`

The required modules which not comes with Python itself can be installed using the 
following command:
```shell
pip install nba_api numpy pandas pyfiglet tabulate termcolor
```

## How to play
To play the game, follow these steps:
1. **Run** the script
2. Follow the **instructions** displayed in the terminal
3. **Guess players** by typing their name and the corresponding number from the grid, as 
shown in the instructions
4. To **quit**, press **CTRL+C** or **CTRL+D**


## Files and functions
### project.py
This is the main file, composed of the following elements:
#### imports
* The first part of the code consists of importing various **libraries** and 
**modules** needed for the program's functionality. It includes libraries for working 
with NBA data, numerical computations, operating system interactions, data 
manipulation, text formatting and more. The typing module is also imported to support 
type hinting.

#### global variables
  * `nba_teams` dictionary containing information from the 30 NBA franchises
  * `scores_emoji` dictionary that translates numbers into emoji

#### class Game
* The Game class represents the core logic of the NBA Hoops Hunch game. This class is 
responsible for managing game state information. The class includes methods and 
properties that allow interaction with the game, as per below:
  - **Attributes**
    - `row_teams` list of team names of grid rows
    - `col_teams` list of team names of grid columns
    - `grid` the game grid represented as a _Pandas DataFrame_
    - `guessed players` number of players who have been guessed so far
  
  - **Methods**
    - `__init__` the constructor of the class that initializes the above attributes
    - `__str__` returns a printable representation of the Game object, printing a 
    welcome banner and the grid
    - `banner` returns a _string_ representing the welcome banner and instructions for 
    the game
    - `is_finished` checks if the game is finished by checking if all players have 
    been guessed
    - `validate_response` checks whether the response given by the user is correct 
    according to the rules of the game
    - `player_is_guessed` checks whether a player has been guessed based on the 
    location and name provided by the user
    - `update_grid` updates the grid with the name of the guessed player based on 
    the location and name provided by the user
  
  - **Properties**
    - `grid` property that returns the _DataFrame_ object representing the game grid
    - `guessed_player` property that returns the number of guessed players

#### main
* This function is used as the primary entry point for program execution when the 
file is run as a script. The `main` contains all the function calls that handle the 
progress of the game and the implementation logic for it.

#### get_teams_played
* This function receives as input the name of an NBA player and returns a list of 
abbreviations of the teams on which that player played during his career.

* `get_teams_played` performs an **online search of the "stats.nba.com" database**, 
using the players module included in the imported API. If the name provided does not 
match a valid player, the _exception_ is handled and an error message is printed. In 
this case, the function returns an empty list, as well as in the case where a player 
also played for teams prior to the founding of the NBA.

#### create_grid
* This function aims to create and initialize a game grid using a _Pandas DataFrame_ 
object. The grid represents three NBA teams organized into rows and columns.

* `create_grid` takes as input two lists: `row` (list of team names for rows) and `col` 
(list of team names for columns) and associates each pair of the elements in these 
lists with an identifying number. The latter will be used by the user to indicate 
which cell of the table he/she intends to complete, providing precise and unambiguous 
input.

#### get_pos_and_name
* This function handles the process of extracting the grid position and player name 
from a user-provided response. The function relies on _regular expressions_ 
to parse the response by extracting the necessary information.

* `get_pos_and_name` receives as input a _string_ representing the response provided by 
the user. Two scenarios can occur at this point:
  - if the user's response matches the pattern defined in the regular expression, the 
  function will return a tuple containing two elements: `pos` (the position in the 
  grid) and `name` (the player's name)
  - if there is no match in the regular expression, the function will return `None`

### test_project.py
* This file was created specifically for use with the `pytest` testing library, with 
the goal of automating and simplifying the process of testing the functions defined in 
the `project.py` file.

### requirements.txt
* This file reports the command lines that must be run from the terminal 
in order to install, via **pip**, the modules necessary for NBA Hoops 
Hunch to work.
