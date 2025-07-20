import unittest

from Allies.AllyGen import AllyGen


class testAllyGen(unittest.TestCase):
    def test_is_nonaligned_no_one(self) -> None:
        self.assertTrue(AllyGen.is_nonaligned('??'))


if __name__ == '__main__':
    unittest.main()
