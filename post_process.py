import pickle
import csv

out_file = open('active_streak_data.csv', 'w', newline='')
# header = ['Name', 'Streak']
writer = csv.writer(out_file)
teammate_master_table = pickle.load(open('teammate_master_table.pkl', 'rb'))
player_streaks = pickle.load(open('player_streaks.pkl', 'rb'))

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