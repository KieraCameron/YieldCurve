import csv
from tabulate import tabulate
import datetime
import matplotlib.pyplot as mat

YIELD_DATA_FILES = ["yield-curve-rates-1990-2024.csv"]#, "yield-curve-rates-2025 (1).csv"]
DATE_LABEL = "Date"

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


class YieldData:
    def __init__(self, filepaths, date_index=0):
        self.files = filepaths
        self.heading, self.array = self.combine_files(filepaths)
        self.numcols = len(self.heading)
        self.numrows = len(self.array)
        self.by_maturity = self.structure_data_by_maturity(self.heading, self.array)
        self.by_date = self.structure_data_by_date(self.array)
        self.dates = self.by_maturity[DATE_LABEL]


    def add_key_in_order(self, dictionary, key, value, order):
        temp_dict = dict()
        index = order.index(key)
        original_keys = list(dictionary.keys())
        for v in original_keys[:index]:
            temp_dict[v] = dictionary[v]
        dictionary[key] = value
        for v in original_keys[index:]:
            temp_dict[v] = dictionary[v]


    def combine_files(self, filepaths):
        full_data = list()
        full_heading = list()
        for filepath in filepaths:
            maturity_dates, raw_data = self.parse_data(filepath)
            if full_heading == list() and full_data == list():
                full_heading = maturity_dates
                full_data += raw_data
                continue
            full_data_by_maturity = self.structure_data_by_maturity(full_heading, full_data)
            raw_data_by_maturity = self.structure_data_by_maturity(heading, raw_data)
            full_data_rows = len(full_data)
            raw_data_rows = len(raw_data)
            if sorted(heading) != sorted(full_heading):

                temp_dict_full = dict() # allows inserted columns to retain the order of the heading
                temp_dict_raw  = dict() # allows inserted columns to retain the order of the heading

                for label in heading:
                    if label in full_heading:
                        temp_dict_full[label] = full_data_by_maturity[label]
                        temp_dict_raw[label] = raw_data_by_maturity[label]
                    else :
                        temp_dict_full[label] = [None] * full_data_rows
                        temp_dict_raw[label] = raw_data_by_maturity[label]

                full_heading = heading
                full_data = self.restructure_to_table(temp_dict_full, "by maturity")
                raw_data = self.restructure_to_table(temp_dict_raw, "by maturity")

            full_data_by_date = self.structure_data_by_date(full_data)
            raw_data_by_date = self.structure_data_by_date(raw_data)

            full_data_dates = list(full_data_by_date.keys())
            raw_data_dates = list(raw_data_by_date.keys())
            new_full_dates = sorted(set(full_data_dates + raw_data_dates))

            temp_dict_full = dict()
            for date in new_full_dates:
                if date in full_data_dates and date in raw_data_dates:
                    if full_data_dates[date] != raw_data_by_date[date]:
                        raise ValueError(f"Date at {date} not equivalent")
                    temp_dict_full[date] = full_data_by_date[date]
                elif date in full_data_dates:
                    temp_dict_full[date] = full_data_by_date[date]
                elif date in raw_data_dates:
                    temp_dict_full[date] = raw_data_dates
                else:
                    raise Exception("wtf")

            full_data = self.restructure_to_table(temp_dict_full, "by date")
        return full_heading, full_data

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
            raw_data[line_number][DATE_LABEL] = self.parse_date(line[DATE_LABEL])
            for mdate in maturity_dates:
                if line[mdate] == "":
                    raw_data[line_number][mdate] = None
                else:
                    raw_data[line_number][mdate] = float(line[mdate])

        if raw_data[0][DATE_LABEL] > raw_data[-1][DATE_LABEL]:
            raw_data = raw_data[::-1]
        return maturity_dates, raw_data

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
        mat.axvspan(datetime.date(2020, 2, 1), datetime.date(2020, 4, 30), color="grey", alpha=0.4, edgecolor=None)  # covid
        mat.axvspan(datetime.date(2007, 12, 1), datetime.date(2009, 6, 30), color="grey", alpha=0.4, edgecolor=None)  # gfc
        mat.axvspan(datetime.date(2001, 3, 1), datetime.date(2001, 11, 30), color="grey", alpha=0.4, edgecolor=None)  # dot-com
        mat.axvspan(datetime.date(1990, 7, 1), datetime.date(1991, 3, 31), color="grey", alpha=0.4, edgecolor=None)  # 1990s


yield_data = YieldData(YIELD_DATA_FILES)

#yield_data.graph(MDate.THREE_MONTH, MDate.TEN_YEAR)
recession_predictor = SpreadGraph(yield_data.dates, yield_data.get_spread(MDate.THREE_MONTH, MDate.TEN_YEAR))

#for date, spread in zip(yield_data.dates,yield_data.get_spread(MDate.THREE_MONTH, MDate.TEN_YEAR)):
#    print(date, spread, sep="\t")

#print(yield_data.heading)
#print(yield_data.by_date[date(2013, 12, 26)])