import gl
import glutils


for gm in gl.gamelogs(2017, 2018):
    tms = gm.teams
    for tm in tms.values():
        if tm.opp.stats['bat']['H'] == 0:
            for player in tm.lineup:
                playerId = player['ID']
                playerName = glutils.getplayername(playerId)
                print(playerId, playerName)

            for tm in tms.values():
                print(tm.linescore, tm.stats['bat'])
