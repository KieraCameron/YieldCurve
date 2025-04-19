class Row:
    def __init__(self, header: list, unique_id, values):
        self.unique_id = unique_id
        self.values = values
        self.header = header

    def __getitem__(self, key):
        if key in self.header:
            index = self.header.find(key)
            return self.values[index]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if key in self.header:
            index = self.header.find(key)
            self.values[index] = value
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __iter__(self):
        for v in self.values:
            yield v

    def __repr__(self):
        return f"Row({self.values})"


class Column:
    def __init__(self, label, unique_ids, values, table):
        self.unique_ids = unique_ids
        self.values = values
        self.label = label
        self.table = table

    def __getitem__(self, key):
        if key in self.unique_ids:
            index = self.unique_ids.find(key)
            return self.values[index]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if key in self.unique_ids:
            index = self.unique_ids.find(key)
            self.values[index] = value
            
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __iter__(self):
        for v in self.values:
            yield v

    def __repr__(self):
        return f"Row({self.values})"


class Table:
    def __init__(self, header: list, unique_ids: list, data=None):
        if len(unique_ids) != len(data):
            raise ValueError("unique ids do not have the same length as data")
        elif len(header) != len(data[0]):  # assume data has values in it
            raise ValueError("number of colums in data should match header")
        self.header = header
        self.unique_ids = unique_ids
        self.data = data
        self.by_column = dict()
        for i, label in enumerate(header):
            self.by_column[label] = [row[i] for row in data]
        self.by_row = dict()
        for i, unique_id in enumerate(unique_ids):
            self.by_row[unique_id] = data[i]

    def __getitem__(self, key):
        if key in self.header:
            return self.by_column[key]
        elif key in self.unique_ids:
            return self.by_column[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __setitem__(self, key, value):
        if key in self.header:
            self.by_column[key] = value
        elif key in self.unique_ids:
            self.by_column[key] = value
        else:
            raise KeyError(f"The key '{key}' does not exist")

