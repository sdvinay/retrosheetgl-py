import retrosheetgl as gl
import glutils

# count and display winners/saver pairs


# map of playerId pairs to array of dates on when they achieved those
winsave_pair_games = {}

for gm in gl.gamelogs(2017, 2019):
    recs = gm.record
    if recs.get('save_pitcher'):
        winsave_pair = (recs['save_pitcher'], recs['winning_pitcher'])
        pair_dates = glutils.getentity(winsave_pair, winsave_pair_games, [])
        pair_dates.append(gm.details['DateStr'])

for winsave_pair in winsave_pair_games:
    if len(winsave_pair_games[winsave_pair]) > 10:
        player_names = map(glutils.getplayername, winsave_pair[0:2])
        print(len(winsave_pair_games[winsave_pair]), tuple(player_names))
