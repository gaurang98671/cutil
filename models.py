import sys
from typing import Optional, Any
import click
import os
import csv
from io import StringIO

class Filter:
    VALID_OPERATIONS={">", ">=", "<", "<=", "==", "contains"}

    def __init__(self, filter:list[str], col_to_index:dict[str, int]):

        if err := self._validate_filter(filter, col_to_index):
            sys.exit(err)
        self.col, self.op, self.val = filter
        self.col_to_index_map = col_to_index

    def _validate_filter(self, filter:tuple[str], col_to_index_map:dict[str, int]) -> str:
        col, op, val = filter
        if op not in Filter.VALID_OPERATIONS:
            return f"{op} is not a valid operations must be one of {Filter.VALID_OPERATIONS}"
        if col not in col_to_index_map:
            return f"{col} does not exists in csv"
        return ""

    def _valid_nums(self, s1:str, s2:str) -> bool:
        return s1.isnumeric() and s2.isnumeric()

    def match(self, row:list[Any]) -> bool:
        i = self.col_to_index_map[self.col]
        
        if len(row) <= i:
            return False
        else:
            row_val = row[i]

        if self.op == "contains":
            return self.val in row_val
        elif self.op == "==":
            return self.val == row_val
        elif self.op == ">":
            return self._valid_nums(self.val, row_val) and float(row_val) > float(self.val)
        elif self.op == "<":
            return self._valid_nums(self.val, row_val) and float(row_val) < float(self.val)
        elif self.op == ">=":
            return self._valid_nums(self.val, row_val) and float(row_val) >= float(self.val)
        elif self.op == "<=":
            return self._valid_nums(self.val, row_val) and float(row_val) <= float(self.val)
        
        return False

class Csv:
    def __init__(self, headers, rows):
        self.rows = rows
        self.headers = headers
        self.col_to_index_map = {header:i for i, header in enumerate(self.headers)}
        
    @classmethod
    def from_csv(self, file:str) -> "Csv":
        if not os.path.isfile(file):
            sys.exit(f"{file} does not exist")
        with open(file , "r") as f:
            data = f.read()
        reader = csv.reader(StringIO(data))
        rows = list(reader)
        headers = rows.pop(0)
        return Csv(headers, rows)

    def display(self, n:int) -> None:
        i = 0
        print(",".join(self.headers) + "\n")
        while i < n and i < len(self.rows):
            print(",".join(self.rows[i]))
            i += 1
    
    def sort(self, col_name:str) -> None:
        col_index = self.col_to_index_map[col_name]
        self.rows.sort(key=lambda x: x[col_index] if len(x) > col_index else float('inf'))

    def filter(self, filter:Filter) -> "Csv":
        filtered_rows = [row for row in self.rows if filter.match(row)]
        return Csv(self.headers, filtered_rows)

    def save(self, output_file_name:str) -> None:
        try:
            with open(output_file_name, "w") as f:
                f.write(",".join(self.headers) + "\n")
                f.write("\n".join([",".join(row) for row in self.rows]))
                print(f"Successfully saved results to {output_file_name}")
        except Exception as e:
            sys.exit(e)

    def aggregate(self, col_name:str, operation:str) -> None:
        if col_name not in self.col_to_index_map:
            sys.exit(f"Column {col_name} does not exist")

        col_index = self.col_to_index_map[col_name]
        vals = [row[col_index] for row in self.rows if len(row) > col_index]
        res = None

        if operation == "sum":
            for v in vals:
                if v.isnumeric():
                    res += float(v)
        elif operation == "avg":
            s, count = 0, 0
            for v in vals:
                if v.isnumeric():
                    s += float(v)
                    count += 1
            res = s / count            
        elif operation == "min":
            for v in vals:
                if not res:
                    res = v
                else:
                    res = min(res, v)
        elif operation == "max":
            for v in vals:
                if not res:
                    res = v
                else:
                    res = max(res, v)
        elif operation == "count":
            res = len(vals)
        else:
            sys.exit(f"{operation} is not a valid aggregation operation")
        
        print(f"{operation} : {res}")