import unittest

from PyRoute.SystemData.SystemStar import SystemStar


class testSystemStar(unittest.TestCase):
    def test_is_bigger(self):
        star1 = SystemStar('V', 'G', 2)
        self.assertEqual('V', star1.size)
        self.assertEqual('G', star1.spectral)
        self.assertEqual(2, star1.digit)
        star2 = SystemStar('VII', 'K', 7)
        self.assertEqual('D', star2.size)
        self.assertEqual('K', star2.spectral)
        self.assertEqual(7, star2.digit)

        self.assertTrue(star1.is_bigger(star2))
        self.assertFalse(star2.is_bigger(star1))


if __name__ == '__main__':
    unittest.main()
