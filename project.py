from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playercareerstats
import numpy as np
import os
import pandas as pd
import pyfiglet
import random
import re
import sys
from tabulate import tabulate
from termcolor import colored
import time
from typing import Union, Tuple

# Global Variables
nba_teams: dict = {
    "ATL": {"name": "Atlanta Hawks", "emoji": "🦅"},
    "BOS": {"name": "Boston Celtics", "emoji": "🍀"},
    "BKN": {"name": "Brooklyn Nets", "emoji": "🌆"},
    "CHA": {"name": "Charlotte Hornets", "emoji": "🐝"},
    "CHI": {"name": "Chicago Bulls", "emoji": "🐮"},
    "CLE": {"name": "Cleveland Cavaliers", "emoji": "🗡️"},
    "DAL": {"name": "Dallas Mavericks", "emoji": "🐴"},
    "DEN": {"name": "Denver Nuggets ", "emoji": "⚒️"},
    "DET": {"name": "Detroit Pistons", "emoji": "🔧"},
    "GSW": {"name": "Golden State Warriors", "emoji": "⚔️"},
    "HOU": {"name": "Houston Rockets", "emoji": "🚀"},
    "IND": {"name": "Indiana Pacers", "emoji": "🏎️"},
    "LAC": {"name": "Los Angeles Clippers", "emoji": "⛵"},
    "LAL": {"name": "Los Angeles Lakers", "emoji": "🎥"},
    "MEM": {"name": "Memphis Grizzles", "emoji": "🐻"},
    "MIA": {"name": "Miami Heat", "emoji": "🔥"},
    "MIL": {"name": "Milwaukee Bucks", "emoji": "🦌"},
    "MIN": {"name": "Minnesota Timberwolves", "emoji": "🐺"},
    "NOP": {"name": "New Orleans Pelicans", "emoji": "⚜️"},
    "NYK": {"name": "New York Knicks", "emoji": "🗽"},
    "OKC": {"name": "Oklahoma City Thunder", "emoji": "🌩️"},
    "ORL": {"name": "Orlando Magic", "emoji": "🔮"},
    "PHI": {"name": "Philadelphia 76ers", "emoji": "🔔"},
    "PHX": {"name": "Phoenix Suns", "emoji": "☀️"},
    "POR": {"name": "Portland Trail Blazers", "emoji": "🌲"},
    "SAC": {"name": "Sacramento Kings", "emoji": "👑"},
    "SAS": {"name": "San Antonio Spurs", "emoji": "🌵"},
    "TOR": {"name": "Toronto Raptors", "emoji": "🍁"},
    "UTA": {"name": "Utah Jazz", "emoji": "🎷"},
    "WAS": {"name": "Washington Wizards", "emoji": "🧙‍♂️"},
}
scores_emoji: dict = {0: '0️⃣', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣',
                      9: '9️⃣'}


class Game:
    def __init__(self, r: list, c: list):
        self.row_teams: list = r
        self.col_teams: list = c
        self.grid: pd.DataFrame = create_grid(self.row_teams, self.col_teams)
        self.guessed_player: int = 0

    @property
    def grid(self) -> pd.DataFrame:
        return self._grid

    @grid.setter
    def grid(self, value: pd.DataFrame):
        self._grid = value

    @property
    def guessed_player(self) -> int:
        return self._guessed_player

    @guessed_player.setter
    def guessed_player(self, value: int):
        self._guessed_player = value

    def __str__(self) -> str:
        # Clear the terminal
        os.system("cls")
        # Print the banner and the grid
        return self.banner() + (tabulate(self.grid, headers='keys', colalign=("center", "center", "center", "center"),
                                         numalign="center", stralign="center", tablefmt='rst'))

    @staticmethod
    def banner() -> str:
        """
        Create the welcome message and instructions for how to play the game

        :return: A multi-line string
        :rtype: str
        """

        # Create the game's title
        figlet = pyfiglet.Figlet()
        figlet.setFont(font="digital")
        title = figlet.renderText("NBA HOOPS HUNCH")

        # Create welcome message
        message: str = ("🏀 Welcome to \033[1mNBA Hoops Hunch\033[0m! 🏀\n"
                        "🎯 \033[1mGoal of the game\033[0m: fill the table with players who have played on both teams "
                        "indicated\n"
                        "🎮 \033[1mControls\033[0m: Keyboard\n"
                        "📄 \033[1mInstructions\033[0m: Type your guess in this format: [1-9] [player's name]\n"
                        "   Type \033[1mCTRL+(C/D) to quit\033[0m the game and see your final score\n"
                        "🍀 \033[3mGood luck!\033[0m 🍀\n")

        return colored(title, "red", "on_cyan", attrs=["bold"]) + "\n" + message

    def is_finished(self) -> bool:
        """
        This method is used to figure out whether the game is finished or not

        :return: Flag which determines whether the grid is completed
        :rtype: bool
        """

        return self.guessed_player == 9

    def validate_response(self, response: str) -> bool:
        """
        This method checks if the given answer is right

        :param response: response prompted by the user
        :type response: str
        :return: A flag
        :rtype: bool
        """

        vals: Tuple[str, str]
        if vals := get_pos_and_name(response):
            # vals is a tuple containing (pos, name)
            return self.player_is_guessed(*vals)

        # If there are no matches, then the response doesn't fit the regex pattern --> it's incorrect
        print("🚫 \033[1mBe careful to type your response as indicated by the instructions!\033[0m")
        time.sleep(2)
        return False

    def player_is_guessed(self, pos: str, name: str):
        """
        This method checks if the player played in both grid's row and col team

        :param pos: Position chosen on the grid
        :param name: Name of the player
        :type pos: str
        :type name: str
        :return: A flag
        :rtype: bool
        """

        # From pos extract row's and col's index (respectively "i" and "j")
        i: np.ndarray
        j: np.ndarray
        i, j = np.where(self.grid.values == pos)

        # Get row team, col team and teams in which the player played in his carrier
        team1: str
        team2: str

        # Check if the grid cell is already filled
        if len(i) == 0 and len(j) == 0:
            print(f"⚠️ \033[1mPosition {pos} is already filled with a valid player!\033[0m")
            time.sleep(2)
            return False

        team1, team2 = self.row_teams[i[0]], self.col_teams[j[0]]
        teams_played: list = get_teams_played(name)
        return (team1 in teams_played) and (team2 in teams_played)

    def update_grid(self, response: str) -> None:
        """
        This method updates the grid by inserting the name of the guessed player in the right position

        :param response: response prompted by the user
        :type response: str
        :return: None
        """

        # Get position in the grid and name of the player
        pos: str
        name: str
        pos, name = get_pos_and_name(response)

        # From pos extract row's and col's index (respectively "i" and "j")
        i: np.ndarray
        j: np.ndarray
        i, j = np.where(self.grid.values == pos)

        # Update the grid in the (i,j) position
        self.grid.iat[i[0], j[0]] = players.find_players_by_full_name(name)[0]["full_name"]


def main():
    # Randomly select three teams per row
    col_teams: list = random.sample(list(nba_teams.keys()), 3)
    # Randomly selects three teams per column, excluding teams already selected by row
    row_teams: list = random.sample(list(filter(lambda x: x not in col_teams, nba_teams.keys())), 3)

    # Instantiate the game object
    game = Game(r=row_teams, c=col_teams)

    while not game.is_finished():
        print(game)

        try:
            # Prompt the user for the response
            response: str = input("Type your guess: ").strip()
        except (EOFError, KeyboardInterrupt):
            # The user wants to quit the game --> break the loop
            break

        if game.validate_response(response):
            print("✅ Well done!")
            # Update the counter and the grid
            game.guessed_player += 1
            game.update_grid(response)
        else:
            print("🔴 Wrong guess! Try again...")

        # Wait 4 seconds before the next iteration
        time.sleep(3)

    # Last print of the grid
    print(game)

    # Check whether the loop was interrupted because the user wanted it to be OR
    # because the grid was entirely completed
    if game.is_finished():
        print("\n🥳 BAAAAAAAAAAAAAAAAAAAAAAAAAAAAANG!!!\n"
              "👌 You completed the grid! Your\033[1m FINAL SCORE\033[0m is 9️⃣/9️⃣\n"
              "🏆 You are the \033[1mNBA Hoops Hunch Champion\033[0m!")
    else:
        print("\n😕 You quit the game!\n"
              f"Your\033[1m FINAL SCORE\033[0m is {scores_emoji[game.guessed_player]}/9️⃣!")

    # Exit with code 0: everything went well!
    sys.exit(0)


def get_teams_played(name: str) -> list:
    """
    Gets the teams (in abbreviation) in which the player played

    :param name: Player's name
    :type name: str
    :return: A list of all the teams in which the player played
    :rtype: list
    """

    # Query the online database, if the name does not exist then handle the Exception
    try:
        player_info = players.find_players_by_full_name(name)
        # Get the player ID
        player_id: str = player_info[0]["id"]
    except:
        print("❓ Who ❓ You typed an invalid name!")
        return []

    # Get the ID of the teams in which the player played
    # NOTE: It must be used filter to exclude teams with ID = 0 (otherwise this would cause a bug)
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    id_teams_played: set = set(filter(lambda x: x != 0, career.get_data_frames()[0]['TEAM_ID'].tolist()))

    # IDs of the 30 NBA actual teams in the database
    teams_id: list = [teams.get_teams()[i]["id"] for i in range(len(teams.get_teams()))]

    # NOTE: The database contains IDs of teams pre-dating the founding of the NBA. It should be checked whether the
    # player in question played exclusively on the 30 teams in today's NBA.
    # (Relocations excluded. For example: Seattle SuperSonics --> Oklahoma City Thunder)
    if all(element in teams_id for element in id_teams_played):
        return sorted(list(map(lambda x: teams.find_team_name_by_id(x)["abbreviation"], id_teams_played)))
    else:
        return []


def create_grid(row: list, col: list) -> pd.DataFrame:
    """
    This function creates and initialises the grid, implemented using a Pandas DataFrame

    :param row: list of row teams
    :param col: list of column teams
    :type row: list
    :type col: list
    :return: the grid formatted as a Pandas DataFrame
    :rtype: pd.DataFrame
    """

    # Concatenate the franchise names with the corresponding emoji
    row: list = list(map(lambda x: nba_teams[x]["name"] + "\n" + nba_teams[x]["emoji"], row))
    col: list = list(map(lambda x: nba_teams[x]["name"] + "\n" + nba_teams[x]["emoji"], col))

    # Set default data in the grid
    data: dict = {
        col[0]: {row[0]: "1", row[1]: "4", row[2]: "7"},
        col[1]: {row[0]: "2", row[1]: "5", row[2]: "8"},
        col[2]: {row[0]: "3", row[1]: "6", row[2]: "9"},
    }

    return pd.DataFrame(data)


def get_pos_and_name(response: str) -> Union[Tuple[str, str], None]:
    """
    This function handles the process of extracting the position in the grid and the player's name

    :param response: response prompted by the user
    :type response: str
    :return: pos and name if there are matches (input fits the regex pattern); if not return None
    :rtype: Tuple[str, str] OR None
    """

    matches: re.Match[str] | None
    # Find matches
    if matches := re.fullmatch(r"^([1-9])\s(.*)$", response, re.IGNORECASE):
        # First captured group is the position
        pos: str = matches.group(1)
        # Second captured group is the player's name prompted by the user
        name: str = matches.group(2)
        return pos, name

    # If there are no matches, return None
    return None


if __name__ == "__main__":
    main()
