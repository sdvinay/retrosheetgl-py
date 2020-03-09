import gl

# Find instances of pitchers saving both games in a doubleheader
# -- finds doubles by putting all saves in a huge list; this is very
#    inefficient and doesn't take advantage of the sorted nature of
#    gamelogs (could reset the list at the start of each day). But
#    we first filter for DHs, this isn't so bad.

saves = []
doubles = []
for gm in gl.gamelogs(1950, 2019):
    if gm.details['GameNum'] > 0:
        if 'save_pitcher' in gm.record:
            tpl = (gm.details['DateStr'], gm.record['save_pitcher'])
            doubles.append(tpl) if tpl in saves else saves.append(tpl)

# aggregate the doubles by pitcher
doubles_by_pitcher = {}
for (dt, pitcher) in doubles:
    gms = gl.getteam(pitcher, doubles_by_pitcher, [])
    gms.append(dt)

# list the pitchers who've done it more than once
for pitcher in doubles_by_pitcher:
    if len(doubles_by_pitcher[pitcher]) > 1:
        print(gl.getplayername(pitcher), doubles_by_pitcher[pitcher])
