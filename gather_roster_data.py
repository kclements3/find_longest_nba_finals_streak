import csv
import requests
from bs4 import BeautifulSoup
import pickle


base_url = 'https://www.basketball-reference.com/'
finals_roster_data = {}


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
    teammatate_url = 'https://www.basketball-reference.com/friv/teammates_and_opponents.fcgi?pid={}&type=t'.format(pid)
    response = requests.get(teammatate_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        raise ('No Response at ' + teammatate_url)

    teammate_table_div = soup.find(id='div_teammates-and-opponents')
    tb = teammate_table_div.find('tbody')
    trs = tb.find_all('tr')

    teammates = []
    for tr in trs:
        if len(tr.attrs) == 0:
            player_div = tr.find(attrs={"data-stat": "pid2"})
            player = player_div.text
            player_url = player_div.find('a')['href'].split('/')
            player_id = player_url[-1].rstrip('.html')
            teammates.append(player_id)
            if player_id not in player_id_name_dir.keys():
                player_id_name_dir[player_id] = player.strip('*')

    return teammates


if __name__ == '__main__':
    try:
        teammates_per_player = pickle.load(open('teammates_per_player', 'rb'))
        player_id_name_dir = pickle.load(open('id_name_map', 'rb'))
    except:
        player_id_name_dir = {}
        teammates_per_player = {}

    # years_to_add = ['2021', '1976', '1975', '1974', '1973', '1972', '1971', '1969', '1968']
    fieldnames = []
    with open('finals_team_data.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # if row['Year'] in years_to_add:
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