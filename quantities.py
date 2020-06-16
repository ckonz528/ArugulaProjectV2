from enum import Enum, auto

volumeLookups = {
    'gal': 3785.41,
    'cup': 236.6,
    'tbsp': 14.78,
    'tsp': 4.92,

    'L': 1000,
    'mL': 1
}


class Unit(Enum):
    COUNT = auto()
    VOLUME = auto()

def roundFrac(val, denominator):
    scaled = int(val * denominator)
    digits = len(str(1.0 / denominator))
    string = f'{{:{digits}f}}'.format(scaled / denominator)
    return string.rstrip('0').rstrip('.')

class Quantity:
    def __init__(self, amount: float, unit: Unit):
        self.amount = amount
        self.unit = unit

    @staticmethod
    def of(val: float, units: str):
        assert units in volumeLookups
        return Quantity(val * volumeLookups[units], Unit.VOLUME)

    @staticmethod
    def count(val: float):
        return Quantity(val, Unit.COUNT)

    def __repr__(self):
        return f'Quantity({self.amount}, {self.unit})'

    def __str__(self):
        if self.unit == Unit.COUNT:
            return roundFrac(self.amount, 4)
        units = sorted(volumeLookups.keys(), key=lambda u: -volumeLookups[u])
        for unit in units:
            if volumeLookups[unit] <= self.amount:
                # return f'{self.amount / volumeLookups[unit]:.2f} {unit}'
                return f'{roundFrac(self.amount / volumeLookups[unit], 4)} {unit}'