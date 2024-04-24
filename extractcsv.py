class CSVData:
    def __init__(self, filepath, has_header=True):
        with open(filepath) as csv_file:
            self.csv_data = csv_file.readlines()

        self.header = self.csv_data[0].strip().split(",")
        self.number_of_columns = len(self.header)
        self.csv_data.pop(0)

        self.parsed_data = self.parse_data(self.csv_data)
        
        self.number_of_rows = len(self.parsed_data)
        

    def parse_data(self, csv_data):
        """convert each line in the csv file into a list"""
        for i in range(len(csv_data)):
            parsed_line = csv_data[i].strip().split(",") # strip removes trailing \n
            while len(parsed_line) < self.number_of_columns:
                parsed_line.append(None)
            if len(parsed_line) > self.number_of_columns:
                raise Exception(", ".join(line) + "\nnumber of values in this line exceeds number of values in header")
            csv_data[i] = parsed_line
        return csv_data

    def extract_by_col(self, parsed_data):
        extracted_data = [[] for _ in range(self.number_of_columns)]
        for i in range(self.number_of_columns):
            for line in parsed_data:
                extracted_data[i].append(line[i])
        return extracted_data

    def format_list(self, lst, func, *indexes):
        if indexes == tuple():
            indexes = range(len(lst))
        for i in indexes:
            if lst[i] == "":
                lst[i] = None
                continue
            lst[i] = func(lst[i])
        return lst

    def convert_to_dict(self, nested_list, key_index):
        dct = dict()
        for lst in nested_list:
            key = lst.pop(key_index)
            dct[key] = lst
        return dct
            
            
if __name__ == "__main__":
    print("runs")
    d = CSVData("Yield Curve Rates 2022 copy.csv")
    d.transposed_data = d.extract_by_col(d.parsed_data)
    def format_date_yield_curve(date):
        import datetime
        month, day, year = date.split("/")
        if len(year) == 2: # some years are YYYY and others are YY.
            if int(year) > 89: # it'll be a long time before 2089 comes around... (and data starts at 1990)
                year = "19" + year
            else:
                year = "20" + year
        return datetime.datetime(int(year), int(month), int(day))

    for i in range(1, len(d.parsed_data)):
        d.parsed_data[i] = d.format_list(d.parsed_data[i], float, *range(1, len(d.parsed_data[i])))
        d.parsed_data[i] = d.format_list(d.parsed_data[i], format_date_yield_curve, 0)
    
    d.transposed_data[0] = d.format_list(d.transposed_data[0], format_date_yield_curve, *range(1, len(d.transposed_data[0])))
    for i in range(1, len(d.transposed_data)):
        d.transposed_data[i] = d.format_list(d.transposed_data[i], float, *range(1, len(d.transposed_data[i])))

    dct_row = d.convert_to_dict(d.parsed_data, 0)
    dct_col = d.convert_to_dict(d.transposed_data, 0)
    for i in dct_col:
        print(i, dct_col[i])
        
            

"""
have a function convert_to_dict that takes parametr key_index,
which sorts the nested list into a dictionary, with the key being the value at key_index in esah list"""


"""
# takes each row, and assigns that to a class.
def extract_by_row(csv_file, parse_date_func=None, parse_string_func=None, date_col=0): #kwargs??
    csv_data = csv_file.readlines()
    header_labels = csv_data[0].strip().split(",") # strip removes trailing \n
    csv_data.pop(0) # gets rid of the header
    for i in range(len(csv_data)):
        data_row = csv_data[i].strip().split(",") # strip removes trailing \n
        if date_col != None:   
            if format_date_func:
                data_row[date_col] = format_date_func(data_row[date_col]) # kwargs might go here
            data_row_copy = data_row[:]
            excluding_date
        for j in range(len(csv_data[i])):
            if csv_data[i][j] == "":
                continue
            days_list[i].yield_values.append(float(csv_data[i][j]))
            days_list[i].maturity_dates.append(maturity_dates_only[j]) # would make more sense to make this a dictionary. Keys are maturity dates. 


def extract_by_col(csv_file):
    \"""assigns data from each column into a dictionary, with the headers as the key\"""
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
