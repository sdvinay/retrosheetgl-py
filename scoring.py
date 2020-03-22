import retrosheetgl as gl
import glutils

G = 'games'
W = 'wins'
L = 'losses'
RS = 'runs_scored'
RA = 'runs_allowed'

teams = {}
empty_team = {G: 0, W: 0, L: 0, RS: 0, RA: 0, 'AB': 0, 'HR': 0}


for gm in gl.gamelogs(2004, 2019):
    if gm.details['ParkID'] == 'SAN02':
        for tm in gm.teams.values():
            team = glutils.getentity(tm.Name, teams, empty_team)
            for category in [RS, RA, W, L, G]:
                team[category] += tm.stats['game'][category]
            team['AB'] += tm.stats['bat']['AB']
            team['HR'] += tm.stats['bat']['HR']


for tm in teams:
    print(tm, teams[tm])
