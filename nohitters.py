import gl
import glutils


# Count the no-hitters that each player has started in

# map of players to the dates of nohitters they've started in
nohitter_starts = {}

for gm in gl.gamelogs(2000, 2019):
    for tm in gm.teams.values():
        if tm.opp.stats['bat'] and tm.opp.stats['bat']['H'] == 0:
            for player in tm.lineup:
                starts = glutils.getentity(player['ID'], nohitter_starts, [])
                starts.append(gm.details['DateStr'])

# print out the players who've started the most no-hitters
for player in nohitter_starts:
    if len(nohitter_starts[player]) > 3:
        print(glutils.getplayername(player), nohitter_starts[player])
