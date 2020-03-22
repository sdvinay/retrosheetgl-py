import retrosheetgl as gl
import glutils

G = 'games'
ATT = 'Attendance'
WEEKDAYS = 'weekdays'
WEEKENDS = 'weekends'
AVG = 'average'
MAX = 'max'
PCT_FULL = 'pct_full'
PCT_EMPTY = 'pct_empty'

parks = {}
days = {WEEKDAYS: ("Mon", "Tue", "Wed", "Thu", "Fri"),
        WEEKENDS: ("Sun", "Sat")}
empty_park = {WEEKDAYS: {G: 0, ATT: 0}, WEEKENDS: {G: 0, ATT: 0}, MAX: 0}


for gm in gl.gamelogs(1993, 2019):
    if ATT in gm.details:
        parkID = gm.details['ParkID']
        wkday = gm.details['DayOfWeek']
        park = glutils.getentity(parkID, parks, empty_park)
        if gm.details[ATT] > park[MAX]: park[MAX] = gm.details[ATT]
        for w in (WEEKDAYS, WEEKENDS):
            if wkday in days[w]:
                park[w][G] += 1
                park[w][ATT] += gm.details[ATT]


def fmtPct(num):
    return "{:.1f}%".format(num*100)


def fmtRatio(num):
    return "{:.2f}".format(num)


for parkID in parks:
    park = parks[parkID]
    for w in (WEEKDAYS, WEEKENDS):
        data = park[w]
        if data[G] > 0:
            data[AVG] = data[ATT]/data[G]
            data[PCT_EMPTY] = 1-data[AVG]/park[MAX]
    if park[WEEKDAYS][G] > 0 and park[WEEKENDS][G] > 0:
        ratio_raw = park[WEEKENDS][AVG] / park[WEEKDAYS][AVG]
        ratio_adj = park[WEEKDAYS][PCT_EMPTY] / park[WEEKENDS][PCT_EMPTY]
        pct_fuller = 1-(park[WEEKENDS][PCT_EMPTY] / park[WEEKDAYS][PCT_EMPTY])
        print(",".join([parkID,
                        fmtRatio(ratio_raw),
                        str(int(park[WEEKDAYS][AVG])),
                        str(int(park[WEEKENDS][AVG])),
                        fmtRatio(ratio_adj),
                        str(park[MAX]),
                        fmtPct(park[WEEKDAYS][PCT_EMPTY]),
                        fmtPct(park[WEEKENDS][PCT_EMPTY]),
                        fmtPct(pct_fuller)]))
print(parks['SAN02'])
