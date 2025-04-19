import csv
from tabulate import tabulate
from datetime import date
import matplotlib.pyplot as mat

YIELD_DATA_FILENAME = "yield-curve-rates-1990-2024.csv"

class MDate: # stands for Maturity Date
    ONE_MONTH = "1 Mo"
    #ONE_AND_HALF_MONTH = "1.5 Mo"
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

# need to be able to combine csvs.

class YieldData:
    def __init__(self, filepath):
        self.filepath = filepath
        self.array = None
        self.heading = None
        with open(filepath) as csvfile:
            raw_data = list(csv.reader(csvfile))
            self.heading, self.array = self.parse_data(raw_data)
        self.by_date = self.structure_data_by_date()
        self.by_maturity = self.structure_data_by_maturity()
        self.numcols = len(self.heading)
        self.numrows = len(self.array)
        self.dates = self.by_maturity["Date"] # should not be string literal


    def __repr__(self):
        dots = [["..."] * self.numcols]
        return tabulate(self.array[:10] + dots + self.array[-10:], headers=self.heading)

    def parse_date(self, date_str):
        month, day, year = date_str.split("/")
        if len(year) == 2:  # some years are YYYY and others are YY.
            if int(year) > 89:  # it'll be a long time before 2089 comes around... (and data starts at 1990)
                year = "19" + year
            else:
                year = "20" + year
        return date(int(year), int(month), int(day))

    def parse_data(self, raw_data):
        for line_number, line in enumerate(raw_data[1:], start=1): # 1: skips the heading
            raw_data[line_number][0] = self.parse_date(line[0])
            for i, yield_interest in enumerate(line[1:], start=1): # 1: skips the date
                if yield_interest == "":
                    raw_data[line_number][i] = None
                else:
                    raw_data[line_number][i] = float(yield_interest)
        return raw_data[0], raw_data[1:]

    def structure_data_by_date(self):
        data_by_date = dict()
        for row in self.array: # 1: skips the heading
            data_by_date[row[0]] = row[1:]
        return data_by_date

    def structure_data_by_maturity(self):
        data_by_maturity = dict()
        for i, label in enumerate(self.heading):
            data_by_maturity[label] = [x[i] for x in self.array]
        return data_by_maturity

    def get_spread(self, short_mdate, long_mdate):
        spread_data = []
        for long, short in zip(self.by_maturity[long_mdate], self.by_maturity[short_mdate]):
            if long is None or short is None:
                spread_data.append(None)
            else:
                spread_data.append(long - short) # round removes python's floating point recursion error
        return spread_data


class SpreadGraph:
    def __init__(self, dates, spread_data):
        self.dates = dates
        self.spread_data = spread_data
        self.figure, self.axes = mat.subplots()
        self.line = self.axes.plot(dates, spread_data)[0]
        self.axes.axhline(0, color="black", linewidth=0.75)
        self.style(highlight_recessions=True)
        mat.show()

    def style(self, highlight_recessions):
        self.line.set_color("orange")
        if highlight_recessions:
            self.highlight_recessions()

    def highlight_recessions(self):
        mat.axvspan(date(2020, 2, 1), date(2020, 4, 30), color="grey", alpha=0.4, edgecolor=None)  # covid
        mat.axvspan(date(2007, 12, 1), date(2009, 6, 30), color="grey", alpha=0.4, edgecolor=None)  # gfc
        mat.axvspan(date(2001, 3, 1), date(2001, 11, 30), color="grey", alpha=0.4, edgecolor=None)  # dot-com
        mat.axvspan(date(1990, 7, 1), date(1991, 3, 31), color="grey", alpha=0.4, edgecolor=None)  # 1990s


yield_data = YieldData(YIELD_DATA_FILENAME)

#yield_data.graph(MDate.THREE_MONTH, MDate.TEN_YEAR)
recession_predictor = SpreadGraph(yield_data.dates, yield_data.get_spread(MDate.THREE_MONTH, MDate.TEN_YEAR))

#for date, spread in zip(yield_data.dates,yield_data.get_spread(MDate.THREE_MONTH, MDate.TEN_YEAR)):
#    print(date, spread, sep="\t")

#print(yield_data.heading)
#print(yield_data.by_date[date(2013, 12, 26)])