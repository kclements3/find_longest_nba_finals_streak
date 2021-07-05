# find_longest_nba_finals_streak
Code used to find the player who has had a teammate in the finals for the most consecutive years.

1. Run scrape_finals_teams.py -> will output finals_team_data.csv
2. Run gather_roster_data.py -> outputs pickle files of id_name_map and teammates_per_player
3. Run main.py -> outputs teammate_master_table.pkl and player_streaks.pkl
4. post_process.py creates a basic dump of active streaks.
