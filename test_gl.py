import retrosheetgl as gl


def test_linescore():
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
