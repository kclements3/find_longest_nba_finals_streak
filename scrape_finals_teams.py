import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.basketball-reference.com/'
csvfile = open('finals_team_data.csv', 'w', newline='')
writer = csv.writer(csvfile)

url = base_url + 'playoffs/'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    raise('No Response at '+url)

finals_table_div = soup.find(id='div_champions_index')
tb = finals_table_div.find('tbody')
trs = tb.find_all('tr')

writer.writerow(['Year', 'Winner', 'RunnerUp', 'WinnerURL', 'RunnerUpURL'])
for tr in trs:
    if len(tr.attrs) == 0:
        year = tr.find(attrs={"data-stat": "year_id"}).text
        champ = tr.find(attrs={"data-stat": "champion"})
        champ_team = champ.text
        if len(champ_team) > 0:
            champ_href = champ.find('a')['href']

            runnerup = tr.find(attrs={"data-stat": "runnerup"})
            runnerup_team = runnerup.text
            runnerup_href = runnerup.find('a')['href']
            writer.writerow([year, champ_team, runnerup_team, champ_href, runnerup_href])

csvfile.close()