import pickle


def find_longest_streak(years):
    # Transform list to integers
    years_int = []
    for y in years:
        years_int.append(int(y))

    streak = 1
    longest_streak = 1
    streak_years = [years_int[0]]
    longest_streak_years = [years_int[0]]
    y_prev = years_int[0]
    if len(years) > 1:
        for y in years_int[1:]:
            if y - y_prev == -1:
                streak += 1
                streak_years.append(y)
            else:
                if streak > longest_streak:
                    longest_streak = streak
                    longest_streak_years = streak_years
                streak = 1
                streak_years = [y]
            y_prev = y
        if streak > longest_streak:
            longest_streak = streak
            longest_streak_years = streak_years
    else:
        longest_streak = 1
        longest_streak_years = streak_years

    return longest_streak, longest_streak_years

if __name__ == '__main__':
    id_name_map = pickle.load(open('id_name_map', 'rb'))
    finals_teammates = pickle.load(open('teammates_per_player', 'rb'))

    teammate_master_table = {}
    for (year, players) in finals_teammates.items():
        for (player, teammates) in players.items():
            teammates_of_player = teammates
            # teammate_master_table[teammate][year]['names'] = []
            # teammate_master_table[teammate][year]['ids'] = []
            for teammate in teammates:
                teammate_master_table.setdefault(teammate, {year: {'names': [], 'ids': []}})
                teammate_master_table[teammate].setdefault(year, {'names': [], 'ids': []})
                teammate_master_table[teammate][year]['names'].append(id_name_map[player])
                teammate_master_table[teammate][year]['ids'].append(player)
    player_streaks = []
    for (teammate, years) in teammate_master_table.items():
        years_w_final_player = sorted(list(years.keys()), reverse=True)
        longest_streak, streak_years = find_longest_streak(years_w_final_player)
        # player_streaks.append((teammate, longest_streak))
        player_streaks.append((id_name_map[teammate], longest_streak, streak_years, teammate))

    player_streaks.sort(key=lambda x:x[1], reverse=True)
    teammate_master_table_f = open('teammate_master_table.pkl', 'wb')
    player_streaks_f = open('player_streaks.pkl', 'wb')
    pickle.dump(teammate_master_table, teammate_master_table_f)
    pickle.dump(player_streaks, player_streaks_f)
    teammate_master_table_f.close()
    player_streaks_f.close()