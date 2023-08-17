from project import *


def test_get_teams_played():
    # NOTE: output lists are sorted alphabetically in ascending order
    assert get_teams_played("LeBron James") == ['CLE', 'LAL', 'MIA']
    assert get_teams_played("lebron") == ['CLE', 'LAL', 'MIA']
    assert get_teams_played("Michael Jordan") == ['CHI', 'WAS']
    assert get_teams_played("Kareem") == ['LAL', 'MIL']
    assert get_teams_played("Kawhi Leonard") == ['LAC', 'SAS', 'TOR']
    assert get_teams_played("Kawhi") == ['LAC', 'SAS', 'TOR']
    assert get_teams_played("P.J. Tucker") == ['HOU', 'MIA', 'MIL', 'PHI', 'PHX', 'TOR']
    assert get_teams_played("Lionel Messi") == []
    assert get_teams_played("Josh Allen") == []


def test_create_grid():
    row_keys = ["LAC", "DEN", "CHI"]
    col_keys = ["BOS", "BKN", "PHI"]

    r = list(map(lambda x: nba_teams[x]["name"] + "\n" + nba_teams[x]["emoji"], row_keys))
    c = list(map(lambda x: nba_teams[x]["name"] + "\n" + nba_teams[x]["emoji"], col_keys))

    data = {
        c[0]: {r[0]: "1", r[1]: "4", r[2]: "7"},
        c[1]: {r[0]: "2", r[1]: "5", r[2]: "8"},
        c[2]: {r[0]: "3", r[1]: "6", r[2]: "9"},
    }
    assert create_grid(row_keys, col_keys).equals(pd.DataFrame(data))


def test_get_pos_and_name():
    assert get_pos_and_name("5 Kobe Bryant") == ("5", "Kobe Bryant")
    assert get_pos_and_name("2 Stephen Curry") == ("2", "Stephen Curry")
    assert get_pos_and_name("9 Terance Mann") == ("9", "Terance Mann")
    assert get_pos_and_name("1 J.J. Barea") == ("1", "J.J. Barea")
    assert get_pos_and_name("3 Kenyon Martin Jr.") == ("3", "Kenyon Martin Jr.")
    assert get_pos_and_name("4 Shaquille O'Neal") == ("4", "Shaquille O'Neal")
    assert get_pos_and_name("6 LeBron") == ("6", "LeBron")
    assert get_pos_and_name("0 LeBron James") is None
    assert get_pos_and_name("10 Paul George") is None
    assert get_pos_and_name("25 Bruce Brown") is None
