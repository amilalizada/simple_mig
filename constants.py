from enum import Enum, auto


class WeightUnit(Enum):
    KG = auto()
    GR = auto()


class OutOfStock(Enum):
    DENY = auto()
    CONTINUE = auto()


class SpecificPriceType(Enum):
    AMOUNT = 'amount'
    PERCENTAGE = 'percentage'
