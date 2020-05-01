import csv

import retrosheetgl as gl
import teammates

expected_counts = {0: 1, 1: 9, 2: 36, 3: 84, 4: 126,
                   5: 126, 6: 84, 7: 36, 8: 9, 9: 1, 10: 0}


def test_teammates():
    gmraw = '"20190320","0","Wed","SEA","AL",1,"OAK","AL",1,9,7,54,"N","","","","OAK01",45787,204,"005130000","112000300",31,7,1,0,2,9,1,1,2,6,0,10,2,1,0,0,5,5,6,6,1,0,27,11,1,0,2,0,35,9,3,0,3,7,0,0,0,3,0,8,0,0,2,0,4,7,9,9,2,0,27,4,0,0,0,0,"nelsj901","Jeff Nelson","gibsh902","Tripp Gibson","barkl901","Lance Barksdale","muchm901","Mike Muchlinski","","(none)","","(none)","servs002","Scott Servais","melvb001","Bob Melvin","gonzm005","Marco Gonzales","fierm001","Michael Fiers","strih001","Hunter Strickland","santd002","Domingo Santana","gonzm005","Marco Gonzales","fierm001","Michael Fiers","gordd002","Dee Gordon",4,"hanim001","Mitch Haniger",8,"brucj001","Jay Bruce",3,"encae001","Edwin Encarnacion",10,"santd002","Domingo Santana",7,"narvo001","Omar Narvaez",2,"healr001","Ryon Healy",5,"beckt001","Tim Beckham",6,"suzui001","Ichiro Suzuki",9,"laurr001","Ramon Laureano",8,"chapm001","Matt Chapman",5,"piscs001","Stephen Piscotty",9,"davik003","Khris Davis",10,"pindc001","Chad Pinder",7,"olsom001","Matt Olson",3,"profj001","Jurickson Profar",4,"semim001","Marcus Semien",6,"hundn001","Nick Hundley",2,"","Y"' # noqa E501
    myreader = csv.reader(gmraw.splitlines())
    for row in myreader:
        tms = gl.parse_game_line(row).teams
        tmH = tms[gl.HA.home]
        for num_common_starters in range(0, 11):
            combos = teammates.teammate_combos(tmH, num_common_starters)
            count = 0
            for mates in combos:
                if num_common_starters > 1:
                    assert mates[0] < mates[1]
                assert len(mates) == num_common_starters
                count += 1
            expected = expected_counts[num_common_starters]
            print(num_common_starters, count, expected)
            assert count == expected


if __name__ == "__main__":
    test_teammates()
