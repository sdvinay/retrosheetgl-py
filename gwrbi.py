import retrosheetgl as gl
import glutils


gwrbis = {}

for gm in gl.gamelogs(1980, 2019):
    if 'gwrbi' in gm.record:
        playerId = gm.record['gwrbi']
        dates = glutils.getentity(playerId, gwrbis, [])
        dates.append(gm.details['DateStr'])

# print out the players with most gwrbi
for player in gwrbis:
    if len(gwrbis[player]) > 100:
        print(glutils.getplayername(player), len(gwrbis[player]))
