import retrosheetgl as gl
import glutils

# count and display winners/saver combinations


# map of playerId pairs to array of dates on when they achieved those combos
combos = {}

for gm in gl.gamelogs(2017, 2019):
    recs = gm.record
    if recs.get('save_pitcher'):
        combo = (recs['save_pitcher'], recs['winning_pitcher'])
        combo_dates = glutils.getentity(combo, combos, [])
        combo_dates.append(gm.details['DateStr'])

for combo in combos:
    if len(combos[combo]) > 10:
        player_names = map(glutils.getplayername, combo[0:2])
        print(len(combos[combo]), tuple(player_names))
