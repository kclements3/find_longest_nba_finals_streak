import pickle


def find_longest_streak(years):
    # Transform list to integers
    years_int = []
    for y in years:
        years_int.append(int(y))

    streak = 1
    longest_streak = 1
    year_end = years_int[0]
    y_prev = years_int[0]
    if len(years) > 1:
        for y in years_int[1:]:
            if y - y_prev == -1:
                streak += 1
            else:
                if streak > longest_streak:
                    longest_streak = streak
                    streak_range = y
                streak = 1
            y_prev = y
        if streak > longest_streak:
            longest_streak = streak
    else:
        longest_streak = 1

    return longest_streak

if __name__ == '__main__':
    id_name_map = pickle.load(open('id_name_map', 'rb'))
    finals_teammates = pickle.load(open('teammates_per_player', 'rb'))

    teammate_master_table = {}
    for (year, players) in finals_teammates.items():
        for (player, teammates) in players.items():
            teammates_of_player = teammates
            for teammate in teammates:
                teammate_master_table.setdefault(teammate, {year: []})
                teammate_master_table[teammate].setdefault(year, [])
                teammate_master_table[teammate][year].append(id_name_map[player])
    player_streaks = []
    for (teammate, years) in teammate_master_table.items():
        years_w_final_player = sorted(list(years.keys()), reverse=True)
        longest_streak = find_longest_streak(years_w_final_player)
        # player_streaks.append((teammate, longest_streak))
        player_streaks.append((id_name_map[teammate], longest_streak, years_w_final_player, teammate))

    player_streaks.sort(key=lambda x:x[1], reverse=True)
    teammate_master_table_f = open('teammate_master_table.pkl', 'wb')
    player_streaks_f = open('player_streaks.pkl', 'wb')
    pickle.dump(teammate_master_table, teammate_master_table_f)
    pickle.dump(player_streaks, player_streaks_f)
    teammate_master_table_f.close()
    player_streaks_f.close()