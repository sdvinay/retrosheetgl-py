import retrosheetgl as gl
import glutils

# count and display winners/saver pairs


# map of playerId pairs to array of dates on when they achieved those
winsave_pairs = {}

for gm in gl.gamelogs(2017, 2019):
    rec = gm.record
    if 'save_pitcher' in rec:
        pair = (rec['save_pitcher'], rec['winning_pitcher'])
        pair_games = glutils.getentity(pair, winsave_pairs, [])
        pair_games.append(gm)

for pair, games in winsave_pairs.items():
    if len(games) > 10:
        player_names = tuple(map(glutils.getplayername, pair))
        print(len(games), player_names)
