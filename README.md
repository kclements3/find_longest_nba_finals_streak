# find_longest_nba_finals_streak
Code used to find the player who has had a teammate in the finals for the most consecutive years.

Until the 2021 NBA finals, Shaquille O'Neal had a teammate in every NBA finals since 1984. 
With his streak over, I'd like to determine who has the next longest active streak.

1. scrape_finals_teams.py: will output finals_team_data.csv
2. gather_roster_data.py: outputs pickle files of id_name_map and teammates_per_player.
   * id_name_map is a key/value dictionary that maps each player id in bbref to a player name.
   * teammates_per_player is a dictionary of the format 
        * {year: {finals player: [list of all teammates]}}
3. main.py: outputs teammate_master_table.pkl and player_streaks.pkl
   * teammate_master_table is a dictionary of the format 
        * player_id: 
            * year:
                * {names: [list of names of teammates for given finals year], ids:[list of all player ids of teammates in finals year]}
   * player_streaks is an ordered list of tuples of the format:
        * (player name, streak length, list of years with a teammate in finals, player_id)
4. post_process.py: creates a basic dump of active streaks called active_streak_data.csv. This can be modified to view different pieces of sterak data if desired.

It turns out that no one has ever had a streak longer than Shaq, and the longest active streak is now held by Jerry Stackhouse.