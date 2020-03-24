import retrosheetgl as gl
import glutils


# Count the shutouts by starting pitchers

# map of players to the dates of nohitters they've started in
shutout_starts = {}
shutout_starts_template = {'wins': 0, 'losses': 0}

for gm in gl.gamelogs(2000, 2019):
    for tm in gm.teams.values():
        if tm.RS == 0:
            starts_loser = glutils.getentity(tm.starter, shutout_starts, shutout_starts_template)
            starts_loser['losses'] += 1
            starts_winner = glutils.getentity(tm.opp.starter, shutout_starts, shutout_starts_template)
            starts_winner['wins'] += 1

# print out the players who've started the most no-hitters
for player in shutout_starts:
    if (shutout_starts[player]['losses']) > 3:
        print(glutils.getplayername(player), shutout_starts[player])
