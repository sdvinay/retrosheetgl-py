import gl

G='games'
O='Outs'

teams = {}
team_template = {G:0, O:0}

for gm in gl.gamelogs(2015):
    for tm in gm['teams']:
        team = gl.getteam(tm['Name'], teams, team_template)
        team[G] += 1
        team[O] += gm[O]

for teamname in teams:
    tm = teams[teamname]
    outputs = (teamname, tm[O], tm[G], tm[O]-54*tm[G])
    print ('|'.join(map(str, outputs)))


