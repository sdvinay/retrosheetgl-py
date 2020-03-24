import retrosheetgl as gl
import glutils
import itertools

# Number of games started together by sets of teammates

NUM_COMMON_STARTERS = 2


def yield_teammate_combos(tm, numTeammates):
    lineup = [player['ID'] for player in tm.lineup]
    for teammates in itertools.combinations(sorted(lineup), numTeammates):
        yield teammates


teammate_numgames = {}
teammate_firstgame = {}
for gm in gl.gamelogs(1969, 2019, "./glfiles/"):
    for tm in gm.teams.values():
        if tm.Name == 'SDN':
            for teammates in yield_teammate_combos(tm, NUM_COMMON_STARTERS):
                if teammates not in teammate_numgames:
                    teammate_numgames[teammates] = 0
                    teammate_firstgame[teammates] = gm.details['DateStr']
                teammate_numgames[teammates] += 1


sorted_d = sorted((value, key) for (key, value) in teammate_firstgame.items())
for (dt, teammates) in sorted_d:
    if teammate_numgames[teammates] > 200:
        playernames = tuple(map(glutils.getplayername, teammates))
        print(teammate_numgames[teammates], dt, playernames)
