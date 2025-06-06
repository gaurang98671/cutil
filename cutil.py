#!/usr/bin/env python
import click
from models import Filter, Csv

@click.command()
@click.argument("file")
@click.option(
    "-n",
    help="Number of rows to display",
    default=5,
    type=click.INT
)
@click.option(
    "--filter",
    help="Filter string in <col_name> <operation> <value> format",
    nargs=3
)
@click.option(
    "-o",
    help="Store results in separate file",
    type=click.STRING,
    default=""
)
@click.option(
    "--aggregate",
    help="Column name and operation",
    nargs=2
)
@click.option(
    "--sort_by",
    help="Colum to sort the results",
    type=click.STRING,
    default=""
)
def process_file(file, n:int, filter:str, o:str, aggregate:tuple[str, str], sort_by:str):

    csv = Csv.from_csv(file)
    filtered_csv = None

    if filter:
        # Not happy with the tight coupling
        # this creates with csv class, but its fine for now
        f = Filter(filter, csv.col_to_index_map)
        csv = csv.filter(f)
    
    if sort_by:
        csv.sort(sort_by)

    # Only display in-case we are not aggregating or storing results into a file
    if not (o or aggregate):
        csv.display(n)
    
    if aggregate:
        csv.aggregate(*aggregate)
    
    if o:
        csv.save(output_file_name=o)

if __name__ == "__main__":
    process_file()