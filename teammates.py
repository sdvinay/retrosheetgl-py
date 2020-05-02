import retrosheetgl as gl
import glutils
import itertools

# Number of games started together by sets of teammates


def teammate_combos(tm, numTeammates):
    lineup = [player['ID'] for player in tm.lineup]
    return itertools.combinations(sorted(lineup), numTeammates)


def summarize_teammate_combos(glsource, num_common, team_filter):
    teammate_numgames = {}
    teammate_firstgame = {}
    for gm in glsource:
        for tm in filter(team_filter, gm.teams.values()):
            for teammates in teammate_combos(tm, num_common):
                if teammates not in teammate_numgames:
                    teammate_numgames[teammates] = 0
                    teammate_firstgame[teammates] = gm.details['DateStr']
                teammate_numgames[teammates] += 1
    return (teammate_numgames, teammate_firstgame)


if __name__ == "__main__":
    glsource = gl.gamelogs(2000, 2019, "./glfiles/")
    NUM_COMMON_STARTERS = 2

    def team_filter(tm): return (tm.Name == 'SDN')
    (teammate_numgames, teammate_firstgame) = summarize_teammate_combos(glsource, NUM_COMMON_STARTERS, team_filter)

    sorted_d = sorted((v, k) for (k, v) in teammate_firstgame.items())
    for (dt, teammates) in sorted_d:
        if teammate_numgames[teammates] > 200:
            playernames = tuple(map(glutils.getplayername, teammates))
            print(teammate_numgames[teammates], dt, playernames)
