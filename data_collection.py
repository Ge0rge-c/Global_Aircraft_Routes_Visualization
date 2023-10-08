"""CSC111 Winter 2023 Project: World Aircraft Routes

Instructions
===============================

This Python module contains a collection of Python functions that is
used in visualize airports and aircraft routes on real world map.

Copyright and Usage Information
===============================

This file is a part of the project used in CSC111 at the University of Toronto
St. George campus.

This file is copyright (c) 2023 Qixuan Chu, Xuanjun Dong, Meizhou Su, Siyu Wu
"""
from __future__ import annotations
import csv
from python_ta.contracts import check_contracts
from airline_graph import AirlineGraph


# @check_contracts
def load_airport_file_ca(airport_file: str) -> AirlineGraph:
    """Return a new airline_graph with airports vertices and no routes in Canada based on given airport file.
    """
    graph = AirlineGraph()
    i = 0

    with open(airport_file, encoding="utf8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row

        for row in reader:
            if row[16] is not None and i > 0:
                graph.add_airport_vertex(airport=str(row[16]),
                                         position=(float(row[4]), float(row[5])),
                                         country='Canada',
                                         province=str(row[12]))
            i += 1
    return graph


# @check_contracts
def load_airport_file_global(airport_file: str) -> AirlineGraph:
    """Return a new airline_graph with airports vertices and no routes worldwide based on given airport file.
    """
    graph = AirlineGraph()

    with open(airport_file, encoding="utf8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row

        for row in reader:
            if len(str(row[4])) != 2:
                graph.add_airport_vertex(airport=str(row[4]),
                                         position=(float(row[6]), float(row[7])),
                                         country=str(row[3]),
                                         province=None)
    return graph


# @check_contracts
def load_route_file(route_file: str, origin_airline_graph: AirlineGraph) -> None:
    """Mutate the completed airline_graph with added routes and corresponding airline nums based on given airline route
    file and given airline_graph with airport vertices

    Preconditions:
        - the origin_airline_graph has had the information of the airports.
    """
    with open(route_file, encoding="utf8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row

        for row in reader:
            if str(row[2]) in origin_airline_graph.get_airports() \
                    and str(row[4]) in origin_airline_graph.get_airports():
                origin_airline_graph.add_route(str(row[2]), str(row[4]), 1)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'airline_graph'],
        'max-line-length': 120,
        'allowed-io': ['load_airport_file_ca', 'load_airport_file_global', 'load_route_file'],
        'disable': ['unused-import']
    })
