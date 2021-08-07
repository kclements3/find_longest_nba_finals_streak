import pickle
import csv
from gather_roster_data import get_career_range

out_file = open('active_streak_data.csv', 'w', newline='')
# header = ['Name', 'Streak']
writer = csv.writer(out_file)
teammate_master_table = pickle.load(open('teammate_master_table.pkl', 'rb'))
player_streaks = pickle.load(open('player_streaks.pkl', 'rb'))
#
active_n = 0
for p in player_streaks:
    if p[2][0] == '2021':
        writer.writerow([p[0], p[1]])
        years = p[2]
        for y in range(int(p[1])):
            writer.writerow([p[2][y], teammate_master_table[p[3]][p[2][y]]])
        active_n += 1
    if active_n > 10:
        break

out_file.close()


## Under construction - not used yet
# career_range_f = open('career_ranges.csv', 'w', newline='')
# player_teams_f = open('player_teams.pkl', 'wb')
# writer = csv.writer(career_range_f)
# # for teammate in teammate_master_table.keys():
# pids = ['onealsh01',
#  'cassesa01',
#  'persowe01',
#  'newmajo01',
#  'parisro01',
#  'nashst01',
#  'luety01',
#  'stackje01',
#  'jonesed02',
#  'davisda01',
#  'reidjr01',
#  'rollitr01',
#  'snower01',
#  'ratlith01',
#  'horryro01',
#  'willike02',
#  'mannida01',
#  'rodmade01',
#  'chambto01',
#  'malonmo01']
#
# player_teams = {}
# for pid in pids:
#     print(pid)
#     [career_range, teams] = get_career_range(pid)
#     writer.writerow([pid, career_range[0], career_range[1]])
#     player_teams[pid] = teams
#
# pickle.dump(player_teams, player_teams_f)
# career_range_f.close()
# player_teams_f.close()