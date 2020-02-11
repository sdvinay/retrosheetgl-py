import gl


for gm in gl.gamelogs(2017, 2018):
    tms = gm.teams
    for tm in tms:
        if tm.opp.stats['bat']['H'] == 0:
            for player in tm.lineup:
                playerId = player['ID']
                playerName = gl.getplayername(playerId)
                print(playerId, playerName)

            for tm in tms:
                print(tm.linescore, tm.stats['bat'])
