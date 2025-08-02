import unittest

from PyRoute.SystemData.UWP import UWP


class testUWP(unittest.TestCase):
    def test_all_question_marks(self):
        uwp = UWP('???????-?')
        self.assertEqual('???????-?', str(uwp))

    def test_all_lowercase(self):
        uwp = UWP('aaaaaaa-a')
        self.assertEqual('AAAAAAA-A', str(uwp))

    def test_canonicalisation_1(self):
        uwp = UWP('aaaaaaa-a')
        uwp.canonicalise()
        self.assertEqual('AAAAAAA-A', str(uwp))

    def test_canonicalisation_2(self):
        uwp = UWP('a1aaaaa-a')
        uwp.canonicalise()
        self.assertEqual('A160AAA-A', str(uwp))

    def test_canonicalisation_3(self):
        uwp = UWP('a0aaaaa-a')
        uwp.canonicalise()
        self.assertEqual('A000AAA-A', str(uwp))

    def test_canonicalisation_4(self):
        uwp = UWP('a2aaaaa-a')
        uwp.canonicalise()
        self.assertEqual('A27AAAA-A', str(uwp))

    def test_canonicalisation_5(self):
        uwp = UWP('x123456-7')
        self.assertEqual('X123456-7', str(uwp))
        uwp.canonicalise()
        self.assertEqual('X120456-7', str(uwp))

    def test_canonicalisation_6(self):
        uwp = UWP('x023456-7')
        self.assertEqual('X023456-7', str(uwp))
        uwp.canonicalise()
        self.assertEqual('X000456-7', str(uwp))

    def test_canonicalisation_7(self):
        uwp = UWP('x1?3456-7')
        self.assertEqual('X1?3456-7', str(uwp))
        uwp.canonicalise()
        self.assertEqual('X1?0456-7', str(uwp))

    def test_canonicalisation_8(self):
        uwp = UWP('x2?4567-8')
        self.assertEqual('X2?4567-8', str(uwp))
        uwp.canonicalise()
        self.assertEqual('X2?4567-8', str(uwp))

    def test_canonicalisation_9(self):
        uwp = UWP('x23?567-8')
        self.assertEqual('X23?567-8', str(uwp))
        uwp.canonicalise()
        self.assertEqual('X23?567-8', str(uwp))

    def test_canonicalisation_10(self):
        uwp = UWP('x023456-?')
        self.assertEqual('X023456-?', str(uwp))
        uwp.canonicalise()
        self.assertEqual('X000456-?', str(uwp))

    def test_canonicalisation_11(self):
        uwp = UWP('x1234?6-7')
        self.assertEqual('X1234?6-7', str(uwp))
        uwp.canonicalise()
        self.assertEqual('X1204?6-7', str(uwp))

    def test_canonicalisation_12(self):
        uwp = UWP('???????-?')
        self.assertEqual('???????-?', str(uwp))
        uwp.canonicalise()
        self.assertEqual('???????-?', str(uwp))

    def test_canonicalisation_13(self):
        uwp = UWP('????1?F-?')
        self.assertEqual('????1?F-?', str(uwp))
        uwp.canonicalise()
        self.assertEqual('????1?B-?', str(uwp))

    def test_canonicalisation_14(self):
        uwp = UWP('??????K-?')
        self.assertEqual('??????K-?', str(uwp))
        uwp.canonicalise()
        self.assertEqual('??????K-?', str(uwp))

    def test_malformed_uwp(self):
        msg = ''
        try:
            UWP('')
        except ValueError as e:
            msg = str(e)
        self.assertEqual('Input UWP malformed', msg)

    def test_malformed_uwp_on_tax_rate(self):
        msg = ''
        try:
            UWP('a2aaaoa-a')
        except ValueError as e:
            msg = str(e)
        self.assertEqual('Input UWP malformed', msg)

    def test_is_well_formed_1(self):
        uwp = UWP('x123456-7')
        result, msg = uwp.is_well_formed()
        self.assertTrue(result)
        self.assertIsNotNone(msg)
        self.assertEqual("", msg)

    def test_is_well_formed_2(self):
        uwp = UWP('x123456-7')
        uwp.gov = None
        result, msg = uwp.is_well_formed()
        self.assertFalse(result)
        self.assertIsNotNone(msg)
        self.assertEqual("String representation wrong length", msg)

    def test_check_canonical_1(self):
        uwp = UWP('aaaaaaa-a')
        exp_msg = []

        result, act_msg = uwp.check_canonical()
        self.assertTrue(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_2(self):
        uwp = UWP('a1aaaaa-a')
        exp_msg = [
            'UWP Calculated atmo "A" not in expected range 0-6',
            'UWP Calculated hydro "A" does not match generated hydro 0'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_3(self):
        uwp = UWP('a0aaaaa-a')
        exp_msg = [
            'UWP Calculated atmo "A" does not match generated atmo 0',
            'UWP Calculated hydro "A" does not match generated hydro 0'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_4(self):
        uwp = UWP('a2aaaaa-a')
        exp_msg = [
            'UWP Calculated atmo "A" not in expected range 0-7'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_5(self):
        uwp = UWP('x123456-7')
        exp_msg = [
            'UWP Calculated hydro "3" does not match generated hydro 0'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_6(self):
        uwp = UWP('x345657-8')
        exp_msg = [
            'UWP Calculated TL "8" not in expected range 2-7'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_6a(self):
        uwp = UWP('x345657-1')
        exp_msg = [
            'UWP Calculated TL "1" not in expected range 2-7'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_7(self):
        uwp = UWP('x345???-F')
        exp_msg = [
            'UWP Calculated TL "F" not in expected range 2-7'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_8(self):
        uwp = UWP('x????D?-F')
        exp_msg = [
            'UWP Calculated TL "F" not in expected range 0-5'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_9(self):
        uwp = UWP('?2?99D?-F')
        exp_msg = [
            'UWP Calculated TL "F" not in expected range 4-9'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_10(self):
        uwp = UWP('???????-F')
        uwp.pop = 'X'
        exp_msg = [
            'UWP Calculated TL "F" not in expected range 1-6'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_11(self):
        uwp = UWP('????F??-F')
        uwp.gov = '1'
        exp_msg = [
            'UWP Calculated gov "1" not in expected range 10-15',
            'UWP Calculated TL "F" not in expected range 6-11'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_12(self):
        uwp = UWP('??19???-F')
        exp_msg = [
            'UWP Calculated hydro "9" not in expected range 0-2',
            'UWP Calculated TL "F" not in expected range 3-8'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_13(self):
        uwp = UWP('??1A1??-F')
        exp_msg = [
            'UWP Calculated hydro "A" not in expected range 0-2',
            'UWP Calculated TL "F" not in expected range 5-10'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_14(self):
        uwp = UWP('???????-?')
        exp_msg = []

        result, act_msg = uwp.check_canonical()
        self.assertTrue(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_15(self):
        uwp = UWP('x023456-7')
        exp_msg = [
            'UWP Calculated atmo "2" does not match generated atmo 0',
            'UWP Calculated hydro "3" does not match generated hydro 0'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_16(self):
        uwp = UWP('x1?3456-7')
        exp_msg = [
            'UWP Calculated hydro "3" does not match generated hydro 0'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_17(self):
        uwp = UWP('x023456-?')
        exp_msg = [
            'UWP Calculated atmo "2" does not match generated atmo 0',
            'UWP Calculated hydro "3" does not match generated hydro 0'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_18(self):
        uwp = UWP('x23?567-8')
        exp_msg = []

        result, act_msg = uwp.check_canonical()
        self.assertTrue(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_19(self):
        uwp = UWP('????1?F-?')
        exp_msg = [
            'UWP Calculated law "F" not in expected range 0-11'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_20(self):
        uwp = UWP('x12391J-7')
        exp_msg = [
            'UWP Calculated hydro "3" does not match generated hydro 0',
            'UWP Calculated gov "1" not in expected range 4-14',
            'UWP Calculated law "J" not in expected range 0-6'
        ]

        result, act_msg = uwp.check_canonical()
        self.assertFalse(result)
        self.assertEqual(exp_msg, act_msg)

    def test_check_canonical_21(self):
        uwp = UWP('??????K-?')
        exp_msg = []

        result, act_msg = uwp.check_canonical()
        self.assertTrue(result)
        self.assertEqual(exp_msg, act_msg)


if __name__ == '__main__':
    unittest.main()
