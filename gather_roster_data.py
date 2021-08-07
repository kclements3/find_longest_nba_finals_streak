import csv
import requests
from bs4 import BeautifulSoup
import pickle


base_url = 'https://www.basketball-reference.com/'
finals_roster_data = {}


def get_career_range(pid):
    url = 'https://www.basketball-reference.com/players/{}/{}.html'.format(pid[0], pid)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        raise ('No Response at ' + url)

    pergame_table_div = soup.find(id='div_per_game')
    tb = pergame_table_div.find('tbody')
    trs = tb.find_all('tr')

    start_ind = 0
    while len(trs[start_ind].attrs) == 0:
        start_ind += 1
    end_ind = -1
    while len(trs[end_ind].attrs) == 0:
        end_ind -= 1

    year1 = trs[start_ind].attrs['id'].split('.')
    year1 = int(year1[1]) - 1

    yearEnd = trs[end_ind].attrs['id'].split('.')
    yearEnd = int(yearEnd[1])

    teams = {}
    for tr in trs:
        if len(tr.attrs) > 0:
            yearDiv = tr.attrs['id'].split('.')
            year = int(yearDiv[1])
            team_div = tr.find(attrs={'data-stat': 'team_id'})
            team = team_div.text
            teams[year] = team

    return [[year1, yearEnd], teams]


def pull_team_roster(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        raise ('No Response at ' + url)

    roster_table_div = soup.find(id='div_roster')
    tb = roster_table_div.find('tbody')
    trs = tb.find_all('tr')

    roster = []
    for tr in trs:
        player_div = tr.find(attrs={"data-stat": "player"})
        player_id = player_div.find('a')['href'].split('/')
        roster.append(player_id[-1].rstrip('.html'))

    return roster


def pull_player_teammates(pid):
    # Get teammates of a given player at the player id associated with input pid.
    teammatate_url = 'https://www.basketball-reference.com/friv/teammates_and_opponents.fcgi?pid={}&type=t'.format(pid)
    response = requests.get(teammatate_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        raise ('No Response at ' + teammatate_url)

    # Find teammate table and pick out all rows
    teammate_table_div = soup.find(id='div_teammates-and-opponents')
    tb = teammate_table_div.find('tbody')
    trs = tb.find_all('tr')

    teammates = []
    # Iterate over all rows in teammate table.
    for tr in trs:
        if len(tr.attrs) == 0:
            # Find
            player_div = tr.find(attrs={"data-stat": "pid2"})
            player = player_div.text
            player_url = player_div.find('a')['href'].split('/')
            player_id = player_url[-1].rstrip('.html')
            teammates.append(player_id)
            if player_id not in player_id_name_dir.keys():
                player_id_name_dir[player_id] = player.strip('*')

    return teammates


if __name__ == '__main__':
    # If this script has alreaday been run, load the teammates_per_player and id_name_map files.
    # If not, initialize as empty dictionaries
    # Note that player_id_name_dir is a
    try:
        teammates_per_player = pickle.load(open('teammates_per_player', 'rb'))
        player_id_name_dir = pickle.load(open('id_name_map', 'rb'))
    except:
        player_id_name_dir = {}
        teammates_per_player = {}

    fieldnames = []
    # Open finals_team_data from scrape_finals_teams.py (must run before this code)
    with open('finals_team_data.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['Year'])
            teammates_per_player.setdefault(row['Year'], {})
            winner_roster = pull_team_roster(base_url + row['WinnerURL'])
            for w in winner_roster:
                teammates = pull_player_teammates(w)
                teammates_per_player[row['Year']][w] = teammates
            loser_roster = pull_team_roster(base_url + row['RunnerUpURL'])
            for l in loser_roster:
                teammates = pull_player_teammates(l)
                teammates_per_player[row['Year']][l] = teammates

            fieldnames.append(row['Year'])
    id_name_map_handler = open('id_name_map', 'wb')
    teammates_per_player_f = open('teammates_per_player', 'wb')
    pickle.dump(player_id_name_dir, id_name_map_handler)
    pickle.dump(teammates_per_player, teammates_per_player_f)
    teammates_per_player_f.close()
    id_name_map_handler.close()