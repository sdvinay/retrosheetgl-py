import csv
import math

import retrosheetgl as gl
import teammates


def test_teammates():
    gmraw = '"20190320","0","Wed","SEA","AL",1,"OAK","AL",1,9,7,54,"N","","","","OAK01",45787,204,"005130000","112000300",31,7,1,0,2,9,1,1,2,6,0,10,2,1,0,0,5,5,6,6,1,0,27,11,1,0,2,0,35,9,3,0,3,7,0,0,0,3,0,8,0,0,2,0,4,7,9,9,2,0,27,4,0,0,0,0,"nelsj901","Jeff Nelson","gibsh902","Tripp Gibson","barkl901","Lance Barksdale","muchm901","Mike Muchlinski","","(none)","","(none)","servs002","Scott Servais","melvb001","Bob Melvin","gonzm005","Marco Gonzales","fierm001","Michael Fiers","strih001","Hunter Strickland","santd002","Domingo Santana","gonzm005","Marco Gonzales","fierm001","Michael Fiers","gordd002","Dee Gordon",4,"hanim001","Mitch Haniger",8,"brucj001","Jay Bruce",3,"encae001","Edwin Encarnacion",10,"santd002","Domingo Santana",7,"narvo001","Omar Narvaez",2,"healr001","Ryon Healy",5,"beckt001","Tim Beckham",6,"suzui001","Ichiro Suzuki",9,"laurr001","Ramon Laureano",8,"chapm001","Matt Chapman",5,"piscs001","Stephen Piscotty",9,"davik003","Khris Davis",10,"pindc001","Chad Pinder",7,"olsom001","Matt Olson",3,"profj001","Jurickson Profar",4,"semim001","Marcus Semien",6,"hundn001","Nick Hundley",2,"","Y"' # noqa E501
    myreader = csv.reader(gmraw.splitlines())
    NUM_COMMON_STARTERS = 3
    for row in myreader:
        tms = gl.parse_game_line(row).teams
        tmH = tms[gl.HA.home]
        combos = teammates.teammate_combos(tmH, NUM_COMMON_STARTERS)
        count = 0
        for mates in combos:
            assert mates[0] < mates[1]
            assert len(mates) == NUM_COMMON_STARTERS
            count += 1
            print(mates)
        print(count)
        assert count == math.comb(9, NUM_COMMON_STARTERS)


if __name__ == "__main__":
    test_teammates()
