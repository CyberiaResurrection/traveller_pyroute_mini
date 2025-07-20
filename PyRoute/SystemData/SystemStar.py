"""
Created on Nov 23, 2023

@author: CyberiaResurrection

"""


class SystemStar(object):

    sizes = ["Ia", "Ib", "II", "III", "IV", "V", "VI", "D", "NS", "PSR", "BH", "BD"]
    starsizes = ["Ia", "Ib", "II", "III", "IV", "V", "VI", "D"]
    spectrals = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    supersizes = ['Ia', 'Ib']

    star_fluxen = {
        'O': {-6: 'Ia', -5: 'Ia', -4: 'Ib', -3: 'II', -2: 'III', -1: 'III', 0: 'III', 1: 'V', 2: 'V', 3: 'V', 4: 'IV', 5: 'D', 6: 'IV', 7: 'IV', 8: 'IV'},
        'B': {-6: 'Ia', -5: 'Ia', -4: 'Ib', -3: 'II', -2: 'III', -1: 'III', 0: 'III', 1: 'III', 2: 'V', 3: 'V', 4: 'IV',
              5: 'D', 6: 'IV', 7: 'IV', 8: 'IV'},
        'A': {-6: 'Ia', -5: 'Ia', -4: 'Ib', -3: 'II', -2: 'III', -1: 'IV', 0: 'V', 1: 'V', 2: 'V', 3: 'V', 4: 'V',
              5: 'D', 6: 'V', 7: 'V', 8: 'V'},
        'F0-4': {-6: 'II', -5: 'II', -4: 'III', -3: 'IV', -2: 'V', -1: 'V', 0: 'V', 1: 'V', 2: 'V', 3: 'V', 4: 'V',
              5: 'D', 6: 'V', 7: 'V', 8: 'V'},
        'F5-9': {-6: 'II', -5: 'II', -4: 'III', -3: 'IV', -2: 'V', -1: 'V', 0: 'V', 1: 'V', 2: 'V', 3: 'V', 4: 'VI',
              5: 'D', 6: 'VI', 7: 'VI', 8: 'VI'},
        'G': {-6: 'II', -5: 'II', -4: 'III', -3: 'IV', -2: 'V', -1: 'V', 0: 'V', 1: 'V', 2: 'V', 3: 'V', 4: 'VI',
              5: 'D', 6: 'VI', 7: 'VI', 8: 'VI'},
        'K': {-6: 'II', -5: 'II', -4: 'III', -3: 'IV', -2: 'V', -1: 'V', 0: 'V', 1: 'V', 2: 'V', 3: 'V', 4: 'VI',
              5: 'D', 6: 'VI', 7: 'VI', 8: 'VI'},
        'M': {-6: 'II', -5: 'II', -4: 'II', -3: 'II', -2: 'III', -1: 'V', 0: 'V', 1: 'V', 2: 'V', 3: 'V', 4: 'VI',
              5: 'D', 6: 'VI', 7: 'VI', 8: 'VI'}
    }

    def __init__(self, size, spectral=None, digit=None):
        self.size = size
        self.spectral = spectral
        self.digit = digit
        if 'VII' == self.size:  # Reclassify archaic degenerate dwarfs as plain dwarfs
            self.size = 'D'

    def is_bigger(self, other) -> bool:
        if self.size != other.size:
            return SystemStar.sizes.index(self.size) < SystemStar.sizes.index(other.size)
        if self.spectral is None or other.spectral is None:
            return True
        if self.spectral != other.spectral:
            return SystemStar.spectrals.index(self.spectral) < SystemStar.spectrals.index(other.spectral)
        if self.digit is None or other.digit is None:
            return True
        if self.digit != other.digit:
            return self.digit < other.digit
        return True
