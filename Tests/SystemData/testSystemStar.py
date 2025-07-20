import unittest

from PyRoute.SystemData.SystemStar import SystemStar


class testSystemStar(unittest.TestCase):
    def test_is_bigger(self):
        star1 = SystemStar('V')
        star2 = SystemStar('VI')

        self.assertTrue(star1.is_bigger(star2))


if __name__ == '__main__':
    unittest.main()
