import matplotlib.pyplot as mat
from matplotlib.animation import FuncAnimation
import math
import datetime
import csv

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

YIELD_CURVE_FILE_PATH = "Yield Curve Rates 1990 - today.csv"
X_AXIS_TICKS = {"1 Mo": 1, "2 Mo": 6, "3 Mo": 11, "4 Mo": 16, "6 Mo": 25, "1 Yr": 45,
                      "2 Yr": 85, "3 Yr": 125, "5 Yr": 165, "7 Yr": 205, "10 Yr": 260,
                      "20 Yr": 360,"30 Yr": 460} # values are lengths between xticks.
                                                 # These will be the x values for the plot
y_limits_per_year = {1990: (2, 10), 1991: (2, 9), 1992: (2, 9), 1993: (2, 9), 1994: (2, 9),
                     1995: (2, 9), 1996: (2, 9), 1997: (2, 9), 1998: (3, 8), 1999: (3, 8), 2000: (3, 7),
                     2001: (0, 7), 2002: (0, 7), 2003: (0, 7), 2004: (0, 6), 2005: (0, 6), 2006: (0, 6),
                     2007: (0, 8), 2008: (0, 8), 2009: (0, 6), 2010: (0, 6), 2011: (0, 6), 2012: (0, 6),
                     2013: (0, 6), 2014: (0, 6), 2015: (0, 6), 2016: (0, 6), 2017: (0, 6), 2018: (0, 6),
                     2019: (0, 6), 2020: (0, 6), 2021: (0, 6), 2022: (0, 6), 2023: (0, 6)}
days_list = []
START_YEAR = 2000
END_YEAR = 2025
SKIP = 1

# all mentions of the variable 'date' refers to a datetime object
# all mentions of the variable 'day' refers to a specific instance of Day
# days is an iterator object that contains a list of Day objects

# test self.date
# get_spread, repr, display spread, yield curve animation, 


class Day:
    def __init__(self, csvrow):
        self.hashed_data = csvrow
        self.date = self.parse_date(self.hashed_data["Date"])
        del self.hashed_data["Date"]
        self.hashed_data = {mdate: (float(value) if value != "" else None)
                            for mdate, value in self.hashed_data.items()}
        # the 1: above skips the date, which has already been parsed and saved.
        self.maturity_dates = self.hashed_data.keys()
        self.yield_values = self.hashed_data.values()

    def parse_date(self, date):
        month, day, year = date.split("/")
        if len(year) == 2:  # some years are YYYY and others are YY.
            if int(year) > 89:  # it'll be a long time before 2089 comes around... (and data starts at 1990)
                year = "19" + year
            else:
                year = "20" + year
        return datetime.datetime(int(year), int(month), int(day))

    def __repr__(self):
        s = self.date.strftime("%d %B, %Y") + "\n"
        s += "\t".join(self.maturity_dates) + "\n"
        s += "\t".join([str(yld) for yld in self.yield_values])
        return s

    def get_spread(self, short_maturity_date, long_maturity_date):
        short_yield = self.hashed_data[short_maturity_date]
        long_yield = self.hashed_data[long_maturity_date]
        if short_yield == None or long_yield == None:
            return None
        else:
            return long_yield - short_yield


def extract_csv_data_col(csv_file):
    """assigns data from each column into a dictionary, with the headers as the key"""
    csv_data = csv_file.readlines()
    header_labels = csv_data[0].strip().split(",") # strip removes trailing \n
    sorted_data = {label: [] for label in header_labels}
    csv_data.pop(0) # gets rid of the header
    for line_index in range(len(csv_data)):
        parsed_data = csv_data[line_index].strip().split(",") # strip removes trailing \n
        while len(parsed_data) < len(header_labels):
            parsed_data.append(None)
        for i, label in enumerate(header_labels):
            sorted_data[label].append(parsed_data[i])

    sorted_data["Date"] = [datetime.datetime.strptime(d, "%Y-%m-%d") for d in sorted_data["Date"]]
    for label in header_labels[1:]:
        for num in range(len(sorted_data[label])):
            if sorted_data[label][num]:
                sorted_data[label][num] = float(sorted_data[label][num])
    return sorted_data

"""
def get_day(start_year=0, end_year=9999, skip=0):
    \"""to be used in conjunction with plot_yield_curve() for the animation\"""
    for s in range(skip+1):
        day = next(days)
    while not start_year <= day.date.year <= end_year:
        for s in range(skip+1):
            day = next(days)

    return day
"""

spx_dict = dict()
with open("spx.csv") as spx_raw_data:
    spx_dict = extract_csv_data_col(spx_raw_data)
    

def filter_dates(start_year, end_year, dates_list):
    start_index = None
    end_index = None
    for i, date in enumerate(dates_list):
        if start_index == None and date.year >= start_year:
            end_index = start_index = i
        if end_year < date.year:
            end_index = i
            break
    else:
        end_index = i
    return start_index, end_index

def highlight_recessions():
    mat.axvspan(datetime.datetime(2020, 2, 1), datetime.datetime(2020, 4, 30), color="grey", alpha=0.4) # covid
    mat.axvspan(datetime.datetime(2007, 12, 1), datetime.datetime(2009, 6, 30), color="grey", alpha=0.4) # gfc
    mat.axvspan(datetime.datetime(2001, 3, 1), datetime.datetime(2001, 11, 30), color="grey", alpha=0.4) # dot-com
    mat.axvspan(datetime.datetime(1990, 7, 1), datetime.datetime(1991, 3, 31), color="grey", alpha=0.4) # 1990s

def display_sp500():
    pass

def display_spread(short_maturity_date, long_maturity_date):
    dates = list()
    yield_values = list()
    
    for day in days_list:
        yield_values.append(day.get_spread(short_maturity_date, long_maturity_date))
        dates.append(day.date)
    
    fig = mat.figure()
    yield_ax = fig.add_subplot(111, label="yield", frame_on=False)
    mat.axhline(y=0, color="black", linewidth=0.75)
    #spx_ax = fig.add_subplot(111, label="spx", frame_on=False)
    


    #start, end = filter_dates(1990, 2024, spx_dict["Date"])
    #earliest = min(spx_dict["Date"][start], dates[0])
    #latest = max(spx_dict["Date"][end-1], dates[-1])
    #spx_ax.set_xlim(earliest, latest)
    #yield_ax.set_xlim(earliest, latest)


    #spx_ax.plot(spx_dict["Date"][start:end], spx_dict["Close"][start:end], label="spx", color="blue")
    yield_ax.plot(dates, yield_values, label="yield", color="orange")
    
    #spx_ax.yaxis.tick_right()

    highlight_recessions()
    
    mat.show()

            

"""def get_y_limits_per_year():
    y_limits_per_year = dict()
    for day in days:
        if day.year not in y_limits_per_year:
            y_limits_per_year[day.date.year] = [10, 0] # [smallest yield, highest yield] on y-axis
        if day.yield_values == []:
            continue
        yield_values_cleaned = [x for x in day.yield_values if x != ""]
        if min(yield_values_cleaned) < y_limits_per_year[day.date.year][0]:
            y_limits_per_year[day.date.year][0] = math.floor(min(yield_values_cleaned))
        
        if max(yield_values_cleaned) > y_limits_per_year[day.date.year][1]:
            y_limits_per_year[day.date.year][1] = math.ceil(max(yield_values_cleaned))
    for i in y_limits_per_year:
        print(i, y_limits_per_year[i])
"""



def plot_yield_curve(framedata):
    day = next(days)
    mat.cla()
    # day = get_day(START_YEAR, END_YEAR, SKIP)
    # mat.xlim(-5, 470)


    # mat.xticks(day.xticks_lengths, day.maturity_dates, rotation=45)
    spread = day.get_spread(MDate.THREE_MONTH, MDate.TEN_YEAR)
    if spread == None or spread >= 0:
        mat.title(day.date.strftime("%B %Y"))
        mat.plot(day.maturity_dates, day.yield_values, marker="o")
    else:
        mat.title(day.date.strftime("%B %Y"), color= "red")
        mat.plot(day.maturity_dates, day.yield_values, marker="o", color= "red")



days_list = []
if __name__ == "__main__":
    with open(YIELD_CURVE_FILE_PATH) as csvfile:
        yield_history = csv.DictReader(csvfile)
        for day in yield_history:
            days_list.append(Day(day))
    days = iter(reversed(days_list))
    """
    yield_curve = extractcsv.CSVData(YIELD_CURVE_FILE_PATH)
    for i in range(1, len(yield_curve.parsed_data)): # start at 1 because first row is the header
        yield_curve.parsed_data[i] = yield_curve.format_list(yield_curve.parsed_data[i], float, *range(1, len(yield_curve.parsed_data[i])))
        yield_curve.parsed_data[i] = yield_curve.format_list(yield_curve.parsed_data[i], format_date_yield_curve, 0)
    
    yield_curve.transposed_data[0] = yield_curve.format_list(yield_curve.transposed_data[0], format_date_yield_curve, *range(1, len(yield_curve.transposed_data[0])))
    for i in range(1, len(yield_curve_data.transposed_data)):
        yield_curve.transposed_data[i] = yield_curve.format_list(yield_curve.transposed_data[i], float, *range(1, len(yield_curve.transposed_data[i])))

    # yield_curve.parsed_data = yield_curve.convert_to_dict(yield_curve.parsed_data, 0)
    # yield_curve.transposed_data = yield_curve.convert_to_dict(yield_curve.transposed_data, 0)
    """
    """
    for line in yield_curve.parsed_data:
        days_list.append(Day(line[0]))
        for yield_value in line[1:]:
            pass
    
    """
    
    #ani = FuncAnimation(mat.gcf(), plot_yield_curve, interval=1, repeat=False)
    #mat.show()
    display_spread(MDate.THREE_MONTH, MDate.TEN_YEAR)
