import unittest

from PyRoute.SystemData.StarList import StarList


class testStarList(unittest.TestCase):

    def test_9_stars_none_trim(self):
        star_line = "G1 V G2 V G3 V G4 V G5 V G6 V G7 V G8 V G9 V"
        msg = None
        try:
            StarList(star_line)
        except ValueError as e:
            msg = str(e)
        self.assertEquals("Max number of stars is 8", msg)

    def test_9_stars_no_trim(self):
        star_line = "G1 V G2 V G3 V G4 V G5 V G6 V G7 V G8 V G9 V"
        msg = None
        try:
            StarList(star_line, trim_stars=False)
        except ValueError as e:
            msg = str(e)
        self.assertEquals("Max number of stars is 8", msg)

    def test_9_stars_trim(self):
        star_line = "G1 V G2 V G3 V G4 V G5 V G6 V G7 V G8 V G9 V"
        star_list = StarList(star_line, trim_stars=True)

        exp_str = "G1 V G2 V G3 V G4 V G5 V G6 V G7 V G8 V"
        act_str = str(star_list)
        self.assertEquals(exp_str, act_str)

    def test_canonicalise_1(self):
        star_line = "G5 V B2 Ia"
        star_list = StarList(star_line)
        self.assertEquals("G5 V B2 Ia", str(star_list))
        star_list.canonicalise()
        self.assertEquals("B2 Ia G5 V", str(star_list))
