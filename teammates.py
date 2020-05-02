import retrosheetgl as gl
import glutils
import itertools

# Number of games started together by sets of teammates


def teammate_combos(tm, numTeammates):
    lineup = [player['ID'] for player in tm.lineup]
    return itertools.combinations(sorted(lineup), numTeammates)


def summarize_teammate_combos(glsource, num_common, team_filter):
    teammate_games = {}
    for gm in glsource:
        for tm in filter(team_filter, gm.teams.values()):
            for teammates in teammate_combos(tm, num_common):
                games = glutils.getentity(teammates, teammate_games, [])
                games.append(gm.details['DateStr'])
    return teammate_games


if __name__ == "__main__":
    glsource = gl.gamelogs(2000, 2019, "./glfiles/")
    NUM_COMMON_STARTERS = 2

    def team_filter(tm): return (tm.Name == 'SDN')
    teammate_games = summarize_teammate_combos(glsource, NUM_COMMON_STARTERS, team_filter)

    for (teammates, games) in teammate_games.items():
        if len(games) > 200:
            playernames = tuple(map(glutils.getplayername, teammates))
            print(len(games), games[0], playernames)
