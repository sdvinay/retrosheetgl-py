import gl

saves = []
doubles = []
for gm in gl.gamelogs(2010, 2019):
    if 'save_pitcher' in gm.record:
        tpl = (gm.details['DateStr'], gm.record['save_pitcher'])
        doubles.append(tpl) if tpl in saves else saves.append(tpl)

for sv in doubles:
    print(sv)
