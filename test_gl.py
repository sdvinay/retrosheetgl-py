import csv

import retrosheetgl as gl
import glutils


def test_parse_linescore():
    parser = gl.parse_linescore_str
    assert parser('0') == [0]
    assert parser('00') == [0, 0]
    assert parser('x') == [None]
    assert parser('1') == [1]
    assert parser('(11)') == [11]
    assert parser('0(11)0') == [0, 11, 0]
    assert parser('0(11)0(20)') == [0, 11, 0, 20]
    assert parser('0(11)(20)0') == [0, 11, 20, 0]
    assert parser('001002030') == [0, 0, 1, 0, 0, 2, 0, 3, 0]


def test_game_details():
    gmraw = '"20190320","0","Wed","SEA","AL",1,"OAK","AL",1,9,7,54,"N","","","","OAK01",45787,204,"005130000","112000300",31,7,1,0,2,9,1,1,2,6,0,10,2,1,0,0,5,5,6,6,1,0,27,11,1,0,2,0,35,9,3,0,3,7,0,0,0,3,0,8,0,0,2,0,4,7,9,9,2,0,27,4,0,0,0,0,"nelsj901","Jeff Nelson","gibsh902","Tripp Gibson","barkl901","Lance Barksdale","muchm901","Mike Muchlinski","","(none)","","(none)","servs002","Scott Servais","melvb001","Bob Melvin","gonzm005","Marco Gonzales","fierm001","Michael Fiers","strih001","Hunter Strickland","santd002","Domingo Santana","gonzm005","Marco Gonzales","fierm001","Michael Fiers","gordd002","Dee Gordon",4,"hanim001","Mitch Haniger",8,"brucj001","Jay Bruce",3,"encae001","Edwin Encarnacion",10,"santd002","Domingo Santana",7,"narvo001","Omar Narvaez",2,"healr001","Ryon Healy",5,"beckt001","Tim Beckham",6,"suzui001","Ichiro Suzuki",9,"laurr001","Ramon Laureano",8,"chapm001","Matt Chapman",5,"piscs001","Stephen Piscotty",9,"davik003","Khris Davis",10,"pindc001","Chad Pinder",7,"olsom001","Matt Olson",3,"profj001","Jurickson Profar",4,"semim001","Marcus Semien",6,"hundn001","Nick Hundley",2,"","Y"'
    myreader = csv.reader(gmraw.splitlines())
    for row in myreader:
        gm = gl.parse_game_line(row)
        assert gm.details['DateStr'] == '20190320'
        assert gm.details['GameNum'] == 0
        assert gm.details['DayOfWeek'] == 'Wed'
        assert gm.details['Outs'] == 54
        assert gm.details['ParkID'] == 'OAK01'
        assert gm.details['Attendance'] == 45787


def test_game_teams():
    gmraw = '"20190320","0","Wed","SEA","AL",1,"OAK","AL",1,9,7,54,"N","","","","OAK01",45787,204,"005130000","112000300",31,7,1,0,2,9,1,1,2,6,0,10,2,1,0,0,5,5,6,6,1,0,27,11,1,0,2,0,35,9,3,0,3,7,0,0,0,3,0,8,0,0,2,0,4,7,9,9,2,0,27,4,0,0,0,0,"nelsj901","Jeff Nelson","gibsh902","Tripp Gibson","barkl901","Lance Barksdale","muchm901","Mike Muchlinski","","(none)","","(none)","servs002","Scott Servais","melvb001","Bob Melvin","gonzm005","Marco Gonzales","fierm001","Michael Fiers","strih001","Hunter Strickland","santd002","Domingo Santana","gonzm005","Marco Gonzales","fierm001","Michael Fiers","gordd002","Dee Gordon",4,"hanim001","Mitch Haniger",8,"brucj001","Jay Bruce",3,"encae001","Edwin Encarnacion",10,"santd002","Domingo Santana",7,"narvo001","Omar Narvaez",2,"healr001","Ryon Healy",5,"beckt001","Tim Beckham",6,"suzui001","Ichiro Suzuki",9,"laurr001","Ramon Laureano",8,"chapm001","Matt Chapman",5,"piscs001","Stephen Piscotty",9,"davik003","Khris Davis",10,"pindc001","Chad Pinder",7,"olsom001","Matt Olson",3,"profj001","Jurickson Profar",4,"semim001","Marcus Semien",6,"hundn001","Nick Hundley",2,"","Y"'
    myreader = csv.reader(gmraw.splitlines())
    for row in myreader:
        tms = gl.parse_game_line(row).teams
        tmH = tms[gl.HA.home]
        tmA = tms[gl.HA.away]
        assert tmH.Name == 'OAK'
        assert tmA.Name == 'SEA'
        assert tmH.opp.Name == 'SEA'
        assert tmA.opp.Name == 'OAK'
        assert tms[~gl.HA.home].Name == 'SEA'
        assert tms[~gl.HA.away].Name == 'OAK'
        assert tmH.RS == 7
        assert tmH.RA == 9
        assert tmA.RS == 9
        assert tmA.RA == 7
        assert tms[~gl.HA.home].RS == 9
        assert tmH.W == 0
        assert tmA.W == 1
        assert tmH.L == 1
        assert tmA.L == 0
        assert tms[~gl.HA.home].L == 0
        (p1, p2) = (tmA.starter, tmH.starter)
        assert p1 == 'gonzm005'
        assert p2 == 'fierm001'
        assert glutils.getplayername(p1) == 'Marco Gonzales'
        assert glutils.getplayername(p2) == 'Michael Fiers'
        assert tmA.linescore == [0, 0, 5, 1, 3, 0, 0, 0, 0]
        assert tmH.linescore == [1, 1, 2, 0, 0, 0, 3, 0, 0]


def test_game_teams_starter_not_record():
    gmraw = '"20190321","0","Thu","SEA","AL",2,"OAK","AL",2,5,4,72,"N","","","","OAK01",46451,267,"021000100001","000020200000",43,9,4,0,2,5,0,1,2,5,0,9,1,0,1,0,10,7,3,3,2,0,36,12,1,0,1,0,46,10,1,0,0,3,0,0,0,6,0,10,0,0,1,0,12,8,5,5,0,1,36,8,0,0,1,0,"welkb901","Bill Welke","barkl901","Lance Barksdale","muchm901","Mike Muchlinski","nelsj901","Jeff Nelson","","(none)","","(none)","servs002","Scott Servais","melvb001","Bob Melvin","rossz001","Zac Rosscup","buchr001","Ryan Buchter","strih001","Hunter Strickland","santd002","Domingo Santana","kikuy001","Yusei Kikuchi","estrm001","Marco Estrada","gordd002","Dee Gordon",4,"hanim001","Mitch Haniger",8,"brucj001","Jay Bruce",3,"encae001","Edwin Encarnacion",10,"santd002","Domingo Santana",7,"narvo001","Omar Narvaez",2,"beckt001","Tim Beckham",6,"healr001","Ryon Healy",5,"suzui001","Ichiro Suzuki",9,"semim001","Marcus Semien",6,"chapm001","Matt Chapman",5,"piscs001","Stephen Piscotty",9,"davik003","Khris Davis",10,"pindc001","Chad Pinder",7,"olsom001","Matt Olson",3,"profj001","Jurickson Profar",4,"laurr001","Ramon Laureano",8,"phegj001","Josh Phegley",2,"","Y"'
    myreader = csv.reader(gmraw.splitlines())
    for row in myreader:
        tms = gl.parse_game_line(row).teams
        (p1, p2) = (tms[~gl.HA.home].starter, tms[gl.HA.home].starter)
        assert p1 == 'kikuy001'
        assert p2 == 'estrm001'
        assert glutils.getplayername(p1) == 'Yusei Kikuchi'
        assert glutils.getplayername(p2) == 'Marco Estrada'
