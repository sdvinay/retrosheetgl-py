import retrosheetgl as gl
import glutils
import itertools

# Number of games started together by sets of teammates


def teammate_combos(tm, numTeammates):
    lineup = [player['ID'] for player in tm.lineup]
    return itertools.combinations(sorted(lineup), numTeammates)


if __name__ == "__main__":
    NUM_COMMON_STARTERS = 2

    teammate_numgames = {}
    teammate_firstgame = {}
    for gm in gl.gamelogs(2000, 2019, "./glfiles/"):
        for tm in gm.teams.values():
            if tm.Name == 'SDN':
                for teammates in teammate_combos(tm, NUM_COMMON_STARTERS):
                    if teammates not in teammate_numgames:
                        teammate_numgames[teammates] = 0
                        teammate_firstgame[teammates] = gm.details['DateStr']
                    teammate_numgames[teammates] += 1

    sorted_d = sorted((v, k) for (k, v) in teammate_firstgame.items())
    for (dt, teammates) in sorted_d:
        if teammate_numgames[teammates] > 200:
            playernames = tuple(map(glutils.getplayername, teammates))
            print(teammate_numgames[teammates], dt, playernames)
