"""Tests for sgf_reader.py."""

from gomill_tests import gomill_test_support

from gomill import sgf_reader

def make_tests(suite):
    suite.addTests(gomill_test_support.make_simple_tests(globals()))


def test_basic_reader(tc):
    sgf = sgf_reader.read_sgf("""\
(;AP[testsuite]CA[utf-8]DT[2009-06-06]FF[4]GM[1]KM[7.5]PB[Black engine]
PL[B]PW[White engine]RE[W+R]SZ[9]AB[ai][bh][ee]AW[fd][gc];B[cg];W[df]C[cmt]
;B[tt]C[Final comment])
""")
    tc.assertEqual(sgf.get_size(), 9)
    tc.assertEqual(sgf.get_komi(), 7.5)
    tc.assertIs(sgf.get_handicap(), None)
    tc.assertEqual(sgf.get_player('b'), "Black engine")
    tc.assertEqual(sgf.get_player('w'), "White engine")
    tc.assertEqual(sgf.get_winner(), 'w')
    tc.assertEqual(sgf.get_root_prop('AP'), "testsuite")
    tc.assertEqual(len(sgf.nodes), 4)
    tc.assertEqual(sgf.nodes[3].get('C'), "Final comment")

def test_malformed(tc):
    def read(s):
        sgf_reader.read_sgf(s)
    tc.assertRaises(ValueError, read, r"")
    tc.assertRaises(ValueError, read, r"(;B[ag]")
    tc.assertRaises(ValueError, read, r"(;B[ag)]")
    tc.assertRaises(ValueError, read, r"(;B[ag\])")
    tc.assertRaises(ValueError, read, r"(B[ag])")
    tc.assertRaises(ValueError, read, r"(;B)")

    # This should fail, but currently we accept it as a propIdent 'B;W'
    #tc.assertRaises(ValueError, read, r"(;B;W[ah])")

    # We don't reject this yet, because we stop at first close-paren
    #tc.assertRaises(ValueError, read, r"(;B[ag];W[ah](;B[ai])")

def test_parsing(tc):
    def check(s):
        sgf = sgf_reader.read_sgf(s)
        return len(sgf.nodes)
    tc.assertEqual(check("(;C[abc]KO[];B[bc])"), 2)
    tc.assertEqual(check("initial junk (;C[abc]KO[];B[bc])"), 2)
    tc.assertEqual(check("(;C[abc]KO[];B[bc]) final junk"), 2)

    tc.assertEqual(check("( ;C[abc]KO[];B[bc])"), 2)
    tc.assertEqual(check("(; C[abc]KO[];B[bc])"), 2)
    tc.assertEqual(check("(;C[abc] KO[];B[bc])"), 2)
    tc.assertEqual(check("(;C[abc]KO[] ;B[bc])"), 2)
    tc.assertEqual(check("(;C[abc]KO[]; B[bc])"), 2)
    tc.assertEqual(check("(;C [abc]KO[];B[bc])"), 2)

    tc.assertEqual(check("(;C[abc]AB[ab][bc];B[bc])"), 2)
    tc.assertEqual(check("(;C[abc]AB[ab] [bc];B[bc])"), 2)

    tc.assertEqual(check("(;C[abc]\nAB[ab]\t[bc];B[bc])"), 2)

    tc.assertEqual(check("(;C[abc]AB[ab][bc](;B[bc]))"), 2)

def test_value_escaping(tc):
    def check(s):
        sgf = sgf_reader.read_sgf(s)
        return sgf.get_root_prop("C")
    tc.assertEqual(check(r"(;C[abc]KO[])"), r"abc")
    tc.assertEqual(check(r"(;C[a\\bc]KO[])"), r"a\bc")
    tc.assertEqual(check(r"(;C[a\\bc\]KO[])"), r"a\bc]KO[")
    tc.assertEqual(check(r"(;C[abc\\]KO[])"), r"abc" + "\\")
    tc.assertEqual(check(r"(;C[xxx :\) yyy]KO[])"), r"xxx :) yyy")

def test_string_handling(tc):
    # NB, read_sgf() currently documents that line endings must be \n
    def check(s):
        sgf = sgf_reader.read_sgf(s)
        return sgf.get_root_prop("C")
    tc.assertEqual(check("(;C[abc ])"), "abc ")
    tc.assertEqual(check("(;C[ab c])"), "ab c")
    tc.assertEqual(check("(;C[ab\tc])"), "ab c")
    tc.assertEqual(check("(;C[ab \tc])"), "ab  c")
    tc.assertEqual(check("(;C[ab\nc])"), "ab\nc")
    tc.assertEqual(check("(;C[ab\\\nc])"), "abc")
    tc.assertEqual(check("(;C[ab\\\\\nc])"), "ab\\\nc")
    tc.assertEqual(check("(;C[ab\xa0c])"), "ab\xa0c")