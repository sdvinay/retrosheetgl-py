import csv
import copy

# TODO not sure why I have these constants but not others
G = 'games'
W = 'wins'
L = 'losses'
RS = 'runs_scored'
RA = 'runs_allowed'

HOME = 1
AWAY = 0

# This player_names map is for convenience, and relatively independent from
# the rest of this module.  Could potentiall make it its own module
player_names = {}


def addplayername(id, name):
    if id not in player_names:
        player_names[id] = name


def getplayername(id):
    return player_names.get(id)


# This getteam is a convenience function, independent from everything else.
# Provides the logic for manging a map of objects/dicts/whatever.
# Doesn't have to be a team; I've used this function for parks, etc., too
def getteam(name, team_dict, team_template):
    if name not in team_dict:
        team_dict[name] = copy.deepcopy(team_template)
    return team_dict[name]


# now we get to the functions actually used for gamelogs
# parse_stats is a relatively generic parser of stat fields
# takes a field_list and starting_field, so it just knows how to parse,
# rather than details of the file
def parse_stats(gmline, field_list, starting_field):
    statmap = {}
    for i in range(len(field_list)):
        stat_name = field_list[i]
        fieldnum = starting_field-1+i
        if (gmline[fieldnum]):
            stat = int(gmline[fieldnum])
            statmap[stat_name] = stat
    return statmap


# parse the starting lineups
# this function has the fieldIDs embedded, and loops across home and away
def parse_lineup(gmline, homeOrAway):
    starting_fields = {HOME: 133, AWAY: 106}
    starting_field = starting_fields.get(homeOrAway)
    lineup = []
    for i in range(9):
        player = {}
        player['ID'] = gmline[starting_field+i*3-1]
        player['position'] = gmline[starting_field+i*3+1]
        lineup.append(player)
        player_name = gmline[starting_field+i*3]
        addplayername(player['ID'], player_name)
    return lineup


# this function translates a linescore representation into a list
# of runs scored by inning
def parse_linescore_str(linestr):
    linescore = []
    i = 0
    while i < len(linestr):
        if(linestr[i] == '('):
            score = int(linestr[i+1:i+3])
            linescore.append(score)
            i += 3
        elif linestr[i] == 'x':
            linescore.append(None)
        else:
            score = int(linestr[i])
            linescore.append(score)
        i += 1
    return linescore


def parse_linescore(gmline, homeOrAway):
    fieldNum = 21-1 if homeOrAway else 20-1
    return parse_linescore_str(gmline[fieldNum])


# parse the players/pitchers of records
# return a dict that can be added to the game obj
def parse_players_of_record(gmline):
    converters = (
            ('winning_pitcher', 94),
            ('losing_pitcher', 96),
            ('save_pitcher', 98),
            # ('gwrbi', 94),
            )
    record = {}
    for converter in converters:
        field = converter[1]
        if (gmline[field-1]):
            record[converter[0]] = gmline[field-1]
            addplayername(gmline[field-1], gmline[field])
    return record


# parses game-level details into a details dict
# TODO should this really be a dict, or should these be attributes on an obj?
def parse_game_details(gmline):
    game_details = {}
    converters = (
        (1, str, 'DateStr'),
        (2, int, 'GameNum'),
        (3, str, 'DayOfWeek'),
        (12, int, 'Outs'),
        (13, str, 'DayNight'),
        (17, str, 'ParkID'),
        (18, int, 'Attendance')
    )
    for converter in converters:
        fieldnum = converter[0]
        func = converter[1]
        stat_name = converter[2]
        datum = gmline[fieldnum-1]  # 1-based index
        if datum:
            converted_data = func(datum)
            game_details[stat_name] = converted_data

    return game_details


def parse_team_stats(gmline, isHomeTeam):
    stat_converters = (
        ('bat', 50, 22),
        ('pitch', 67, 39),
        ('field', 72, 44),
    )
    stat_fields = {}
    stat_fields['bat'] = (
            'AB', 'H', '2B', '3B', 'HR', 'RBI', 'SH', 'SF', 'HBP',
            'BB', 'IBB', 'SO', 'SB', 'CS', 'GDP', 'CI', 'LOB')
    stat_fields['pitch'] = ('NumPitchers', 'IndivER', 'ER', 'WP', 'BK')
    stat_fields['field'] = ('PO', 'A', 'E', 'PB', 'DP', 'TP')

    team_dict = {}
    for converter in stat_converters:
        fieldnum = converter[1] if isHomeTeam else converter[2]
        stats_type = converter[0]
        fields = stat_fields[stats_type]
        team_dict[stats_type] = parse_stats(gmline, fields, fieldnum)
    return team_dict


class Team:
    def __init__(self):
        pass


class Game:
    def __init__(self):
        self.teams = [Team(), Team()]
        self.details = {}
        self.record = {}


def parse_game_line(gmline):
    gm = Game()
    tms = gm.teams
    tms[HOME].opp = tms[AWAY]
    tms[AWAY].opp = tms[HOME]

    tms[HOME].G = tms[AWAY].G = 1

    gm.details = parse_game_details(gmline)

    tms[HOME].Name = gmline[7-1]
    tms[AWAY].Name = gmline[4-1]
    tms[HOME].RS = tms[AWAY].RA = int(gmline[11-1])
    tms[HOME].RA = tms[AWAY].RS = int(gmline[10-1])
    tms[HOME].W = tms[HOME].L = tms[AWAY].W = tms[AWAY].L = 0
    if tms[HOME].RS > tms[AWAY].RS: tms[HOME].W = tms[AWAY].L = 1
    if tms[HOME].RS < tms[AWAY].RS: tms[HOME].L = tms[AWAY].W = 1

    for homeOrAway in (HOME, AWAY):
        tm = tms[homeOrAway]
        tm.stats = parse_team_stats(gmline, homeOrAway)
        tm.stats['game'] = {G: tm.G, W: tm.W, L: tm.L, RS: tm.RS, RA: tm.RA}
        tm.lineup = parse_lineup(gmline, homeOrAway)
        tm.linescore = parse_linescore(gmline, homeOrAway)

    gm.record = parse_players_of_record(gmline)

    return gm


def get_gl_filename(year):
    return 'glfiles/GL{}.TXT'.format(year)


def gamelogs(firstyear, lastyear=None):
    years = range(firstyear, lastyear+1) if lastyear else [firstyear]
    for year in years:
        with open(get_gl_filename(year)) as glfile:
            for gmline in csv.reader(glfile):
                gm = parse_game_line(gmline)
                gm.year = year
                yield gm
