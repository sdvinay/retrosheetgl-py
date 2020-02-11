import gl


combos = {}
for gm in gl.gamelogs(2019):
    recs = gm['record']
    if recs.get('save_pitcher'):
        combo = (recs['save_pitcher'], recs['winning_pitcher'], gm['year'])
        if combo not in combos:
            combos[combo] = 0
        combos[combo] += 1

for combo in combos:
    if combos[combo] > 3:
        print(combos[combo], tuple(map(gl.getplayername, combo[0:2])), combo[2])
