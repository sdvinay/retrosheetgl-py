import gl
import glutils
import itertools

teammate_games = {}
for gm in gl.gamelogs(2018, 2019):
    for tm in gm.teams:
        lineup = tm.lineup
        for combo in itertools.combinations(lineup, 2):
            pair = (combo[0]['ID'], combo[1]['ID'])
            if pair not in teammate_games:
                teammate_games[pair] = 0
            teammate_games[pair] += 1


for pair in teammate_games:
    print(teammate_games[pair], tuple(map(glutils.getplayername, pair)))
