# Setup
```
pip install -r requirements.txt
chmod +x ./cutil.py
```

# How to run?
Runing script with file name will display 5 rows
```
./cutil.py file.csv
```

Display multiple rows
```
./cutil.py file.csv -n 30
```

## Usage
```
$ ./cutil.py --help
Usage: cutil.py [OPTIONS] FILE

Options:
  -n INTEGER           Number of rows to display
  --filter TEXT...     Filter string in <col_name> <operation> <value> format
  -o TEXT              Store results in separate file
  --aggregate TEXT...  Column name and operation
  --sort_by TEXT       Colum to sort the results
  --help               Show this message and exit
```

## Filtering
Use `--filter <column_name> <operation> <value>` to filter rows
Operations can be `contains`, `==`, `<`, `>`, `<=` and `>=`
Example
```
./cutil.py sample.csv --filter "First Name" contains Sh
```

## Aggregate
Use `--aggregate <col_name> <operation>` to aggregate colum values
Operations can be `sum`, `avg`, `min` or `max`
In case `--filter` was applied, aggregation will be done on filtered values
Example
```
./cutil.py sample.csv --aggregate Index sum
./cutil.py sample2.csv --filter Age > 30 --aggregate Salary avg
```

## Sorting
Use `--sory_by <column_name>` to sort the results
Example
```
./cutil.py sample.csv --sort_by "First Name"
```

## Store results
Use `-o <output_file_name>` to store the results in separate csv file
Example
```
./cutil.py sample.csv --filter "First Name" contains Sh -o op.csv
``` 

## Examples
Display all less than equal to index 10
Node: Add "<" for arrow operators as shell will confuse it for redirects 
```
./cutil.py sample.csv --filter Index "<=" 10 -n 100 
```

Get min/max value for column
```
# For strings it will print lexographically min/max value
./cutil.py sample.csv --aggregate "First Name" min

./cutil.py sample.csv --aggregate Index max
```

Aggregate filtered value
```
./cutil sample.csv --filter Country == Poland --aggregate Index min
```