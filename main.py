import csv
from tabulate import tabulate

import matplotlib.pyplot as plt

YIELD_DATA_FILENAME = "Yield Curve Rates 1990 - today.csv"

class MDate: # stands for Maturity Date
    ONE_MONTH = "1 Mo"
    ONE_AND_HALF_MONTH = "1.5 Mo"
    TWO_MONTH = "2 Mo"
    THREE_MONTH = "3 Mo"
    FOUR_MONTH = "4 Mo"
    SIX_MONTH = "6 Mo"
    ONE_YEAR = "1 Yr"
    TWO_YEAR = "2 Yr"
    THREE_YEAR = "3 Yr"
    FIVE_YEAR = "5 Yr"
    SEVEN_YEAR = "7 Yr"
    TEN_YEAR = "10 Yr"
    TWENTY_YEAR = "20 Yr"
    THIRTY_YEAR = "30 Yr"

class Data:
    def __init__(self, filepath):
        self.filepath = filepath
        self.raw = list()
        with open(filepath) as csvfile:
            for row in csv.reader(csvfile):
                self.raw.append(row)
        self.numrows = len(self.raw)
        self.numcols = len(self.raw[0])


    def __repr__(self):
        dots = [["..."] * self.numcols]
        return tabulate(self.raw[1:11] + dots + self.raw[-10:], headers=self.raw[0])



yield_data = Data(YIELD_DATA_FILENAME)
