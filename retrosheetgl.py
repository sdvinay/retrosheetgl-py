import csv
import glutils
from enum import Flag, auto

GLFILE_DIR = './glfiles/'

# TODO not sure why I have these constants but not others
G = 'games'
W = 'wins'
L = 'losses'
RS = 'runs_scored'
RA = 'runs_allowed'


class HA(Flag):
    home = auto()
    away = 0


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


# parse a starting lineups
# this function "knows" the format and fieldnums for each team's lineup
def parse_lineup(gmline, homeOrAway):
    starting_field = {HA.home: 133, HA.away: 106}[homeOrAway]

    def createPlayer(i):
        player = {}
        player['ID'] = gmline[starting_field+i*3-1]
        player['position'] = gmline[starting_field+i*3+1]
        player_name = gmline[starting_field+i*3]
        glutils.addplayername(player['ID'], player_name)
        return player
    lineup = [createPlayer(i) for i in range(9)]
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
    fieldNum = {HA.home: 21, HA.away: 20}[homeOrAway] - 1
    return parse_linescore_str(gmline[fieldNum])


# parse the players/pitchers of records
# return a dict that can be added to the game obj
def parse_players_of_record(gmline):
    converters = (
            ('winning_pitcher', 94),
            ('losing_pitcher', 96),
            ('save_pitcher', 98),
            ('gwrbi', 100),
            )
    record = {}
    for (fieldname, fieldnum) in converters:
        val = gmline[fieldnum-1]
        if val:
            record[fieldname] = val
            glutils.addplayername(val, gmline[fieldnum])
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


def parse_team_stats(gmline, homeOrAway):
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
        fieldnum = converter[1] if homeOrAway == HA.home else converter[2]
        stats_type = converter[0]
        fields = stat_fields[stats_type]
        team_dict[stats_type] = parse_stats(gmline, fields, fieldnum)
    return team_dict


class Team:
    def __init__(self):
        pass


class Game:
    def __init__(self):
        self.teams = {HA.home: Team(), HA.away: Team()}
        self.details = {}
        self.record = {}


def parse_game_line(gmline):
    gm = Game()
    tms = gm.teams
    tms[HA.home].opp = tms[HA.away]
    tms[HA.away].opp = tms[HA.home]

    gm.details = parse_game_details(gmline)

    for (homeOrAway, tm) in tms.items():
        tm.Name = gmline[{HA.home: 7, HA.away: 4}[homeOrAway]-1]
        tm.G = 1
        tm.RS = tm.opp.RA = int(gmline[{HA.home: 11, HA.away: 10}[homeOrAway]-1])
        tm.stats = parse_team_stats(gmline, homeOrAway)
        tm.lineup = parse_lineup(gmline, homeOrAway)
        tm.linescore = parse_linescore(gmline, homeOrAway)
        SP_fieldnum = {HA.home: 104, HA.away: 102}[homeOrAway]
        tm.starter = gmline[SP_fieldnum-1]
        glutils.addplayername(tm.starter, gmline[SP_fieldnum])

    tms[HA.home].W = tms[HA.home].L = tms[HA.away].W = tms[HA.away].L = 0
    if tms[HA.home].RS > tms[HA.away].RS: tms[HA.home].W = tms[HA.away].L = 1
    if tms[HA.home].RS < tms[HA.away].RS: tms[HA.home].L = tms[HA.away].W = 1

    for tm in tms.values():
        tm.stats['game'] = {G: tm.G, W: tm.W, L: tm.L, RS: tm.RS, RA: tm.RA}

    gm.record = parse_players_of_record(gmline)

    return gm


def get_gl_filename(dir, year):
    return '{DIR}/GL{YR}.TXT'.format(DIR=dir, YR=year)


def gamelogs(firstyear, lastyear=None, glfile_dir=GLFILE_DIR):
    years = range(firstyear, lastyear+1) if lastyear else [firstyear]
    for year in years:
        with open(get_gl_filename(glfile_dir, year)) as glfile:
            for gmline in csv.reader(glfile):
                gm = parse_game_line(gmline)
                gm.year = year
                yield gm
