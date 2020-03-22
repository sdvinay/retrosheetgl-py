import retrosheetgl as gl
import glutils


combos = {}
for gm in gl.gamelogs(2019):
    recs = gm.record
    if recs.get('save_pitcher'):
        combo = (recs['save_pitcher'], recs['winning_pitcher'], gm.year)
        if combo not in combos:
            combos[combo] = 0
        combos[combo] += 1

for combo in combos:
    if combos[combo] > 3:
        player_names = map(glutils.getplayername, combo[0:2])
        print(combos[combo], tuple((player_names, combo[2])))
