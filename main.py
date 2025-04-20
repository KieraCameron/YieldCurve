import csv

from matplotlib.animation import FuncAnimation
from tabulate import tabulate
import datetime
import matplotlib.pyplot as mat

YIELD_DATA_FILES = ["yield-curve-rates-1990-2024.csv", "yield-curve-rates-2025 (1).csv"]
FULL_HEADING = ["1 Mo","1.5 Mo","2 Mo","3 Mo","4 Mo","6 Mo","1 Yr",
                "2 Yr","3 Yr","5 Yr","7 Yr","10 Yr","20 Yr","30 Yr"]
DATE = "Date"

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

class Day:
    def __init__(self, csvrow):
        self.as_dict = csvrow
        self.date = self.parse_date(self.as_dict[DATE])
        del self.as_dict[DATE]
        self.as_dict = {mdate: (float(value) if value != "" else None)
                        for mdate, value in self.as_dict.items()}
        self.maturity_dates = list(self.as_dict.keys())
        if MDate.ONE_AND_HALF_MONTH not in self.maturity_dates:
            self.add_key_in_order()
        self.yield_values = list(self.as_dict.values())

    def parse_date(self, date):
        month, day, year = date.split("/")
        if len(year) == 2:  # some years are YYYY and others are YY.
            if int(year) > 89:  # it'll be a long time before 2089 comes around... (and data starts at 1990)
                year = "19" + year
            else:
                year = "20" + year
        return datetime.date(int(year), int(month), int(day))

    def __repr__(self):
        s = self.date.strftime("%d %B, %Y") + "\n"
        s += "\t".join(self.maturity_dates) + "\n"
        s += "\t".join([str(yld) for yld in self.yield_values])
        return s

    def get_spread(self, short_maturity_date, long_maturity_date):
        short_yield = self.as_dict[short_maturity_date]
        long_yield = self.as_dict[long_maturity_date]
        if short_yield == None or long_yield == None:
            return None
        else:
            return long_yield - short_yield

    def add_key_in_order(self, key=MDate.ONE_AND_HALF_MONTH):
        temp_dict = dict()
        index = FULL_HEADING.index(key)
        original_keys = self.maturity_dates
        for v in original_keys[:index]:
            temp_dict[v] = self.as_dict[v]
        self.as_dict[key] = None
        for v in original_keys[index:]:
            temp_dict[v] = self.as_dict[v]
        self.as_dict = temp_dict
        self.maturity_dates = FULL_HEADING


"""
class YieldData:
    def __init__(self, filepaths):
        self.files = filepaths

        self.numcols = len(self.heading)
        self.numrows = len(self.array)
        self.dates = [day[DATE] for day in self.array]

    def combine_files(self, filepaths):
        full_data = list()
        full_maturity_dates = set()
        for filepath in filepaths:
            maturity_dates, raw_data = self.parse_data(filepath)
            if full_maturity_dates == set() and full_data == list():
                full_maturity_dates = maturity_dates
                full_data += raw_data
                continue
            else:
                full_maturity_dates = full_maturity_dates.union(maturity_dates)
                not_in_full = maturity_dates.difference(full_maturity_dates)

                for daynumber, day in enumerate(full_data):
                    for mdate in not_in_full:
                        full_data[daynumber][mdate] = None

                not_in_raw = full_maturity_dates.difference(maturity_dates)

                for daynumber, day in enumerate(raw_data):
                    for mdate in not_in_raw:
                        raw_data[daynumber][mdate] = None

            full_data += raw_data


        return full_maturity_dates, full_data

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
        return datetime.date(int(year), int(month), int(day))

    def parse_data(self, filepath):
        with open(filepath) as csvfile:
            raw_data = list(csv.DictReader(csvfile))
            maturity_dates = list(raw_data[0].keys())[1:]
        for line_number, line in enumerate(raw_data):
            raw_data[line_number][DATE] = self.parse_date(line[DATE])
            for mdate in maturity_dates:
                if line[mdate] == "":
                    raw_data[line_number][mdate] = None
                else:
                    raw_data[line_number][mdate] = float(line[mdate])

        if raw_data[0][DATE] > raw_data[-1][DATE]:
            raw_data = raw_data[::-1]
        return set(maturity_dates), raw_data

    def restructure_to_table(self, data_structure: dict, structure_type):
        table_structure = list()
        if structure_type == "by date":
            for date, values in data_structure.items():
                table_structure.append([date] + values)
        elif structure_type == "by maturity":
            for i, _ in enumerate(data_structure["Date"]):
                table_structure.append([])
                for key in data_structure:
                    table_structure[i].append(data_structure[key][i])
        else:
            raise TypeError("Structure type doesnt exist")
        return table_structure

    def structure_data_by_date(self, array):
        data_by_date = dict()
        for row in array:
            data_by_date[row[0]] = row[1:]
        return data_by_date

    def structure_data_by_maturity(self, heading, array):
        data_by_maturity = dict()
        for i, label in enumerate(heading):
            data_by_maturity[label] = [x[i] for x in array]
        return data_by_maturity

    def get_spread(self, short_mdate, long_mdate):
        long_array = [day[long_mdate] for day in self.array]
        short_array = [day[short_mdate] for day in self.array]

        spread_data = []
        for long, short in zip(long_array, short_array):
            if long is None or short is None:
                spread_data.append(None)
            else:
                spread_data.append(long - short) # round removes python's floating point recursion error
        return spread_data
"""

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
        mat.axvspan(datetime.date(2020, 2, 1), datetime.date(2020, 4, 30), color="grey", alpha=0.4, edgecolor=None)  # covid
        mat.axvspan(datetime.date(2007, 12, 1), datetime.date(2009, 6, 30), color="grey", alpha=0.4, edgecolor=None)  # gfc
        mat.axvspan(datetime.date(2001, 3, 1), datetime.date(2001, 11, 30), color="grey", alpha=0.4, edgecolor=None)  # dot-com
        mat.axvspan(datetime.date(1990, 7, 1), datetime.date(1991, 3, 31), color="grey", alpha=0.4, edgecolor=None)  # 1990s

days_list = []
for filepath in YIELD_DATA_FILES:
    with open(filepath) as raw_data:
        raw_data = list(csv.DictReader(raw_data))
        for line in raw_data[::-1]:
            days_list.append(Day(line))

days_iter = iter(days_list)


#recession_predictor = SpreadGraph(yield_data.dates, yield_data.get_spread(MDate.THREE_MONTH, MDate.TEN_YEAR))
fig, ax = mat.subplots()

def plot_yield_curve(framedata):
    mat.cla()
    day = next(days_iter)
    yields = day.yield_values
    date = day.date
    spread = day.get_spread(MDate.THREE_MONTH, MDate.TEN_YEAR)
    print(len(FULL_HEADING[1:]), len(yields))
    if spread == None or spread >= 0:
        mat.title(date.strftime("%B %Y"))
        ax.plot(FULL_HEADING[1:], yields, marker="o")
    else:
        mat.title(date.strftime("%B %Y"), color= "red")
        ax.plot(FULL_HEADING[1:], yields, marker="o", color= "red")

ani = FuncAnimation(mat.gcf(), plot_yield_curve, interval=1, repeat=False)
mat.show()


#for date, spread in zip(yield_data.dates,yield_data.get_spread(MDate.THREE_MONTH, MDate.TEN_YEAR)):
#    print(date, spread, sep="\t")

#print(yield_data.heading)
#print(yield_data.by_date[date(2013, 12, 26)])