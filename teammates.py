import gl
import glutils
import itertools

# Number of games started together by sets of teammates

NUM_COMMON_STARTERS = 2


def yield_teammate_combos(gm, numTeammates):
    for tm in gm.teams.values():
        lineup = [player['ID'] for player in tm.lineup]
        for teammates in itertools.combinations(sorted(lineup), numTeammates):
            yield teammates


teammate_numgames = {}
teammate_firstgame = {}
for gm in gl.gamelogs(2000, 2019):
    for teammates in yield_teammate_combos(gm, NUM_COMMON_STARTERS):
        if teammates not in teammate_numgames:
            teammate_numgames[teammates] = 0
            teammate_firstgame[teammates] = gm.details['DateStr']
        teammate_numgames[teammates] += 1


sorted_d = sorted((value, key) for (key, value) in teammate_firstgame.items())
for (dt, teammates) in sorted_d:
    if teammate_numgames[teammates] > 500:
        playernames = tuple(map(glutils.getplayername, teammates))
        print(teammate_numgames[teammates], dt, playernames)
