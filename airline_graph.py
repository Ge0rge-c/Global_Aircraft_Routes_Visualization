"""CSC111 Winter 2023 Project: World Aircraft Routes

Instructions
===============================

This Python module contains a collection of Python classes and functions that is
used for building graph and connections between airports.

Copyright and Usage Information
===============================

This file is a part of the project used in CSC111 at the University of Toronto
St. George campus.

This file is copyright (c) 2023 Qixuan Chu, Xuanjun Dong, Meizhou Su, Siyu Wu
"""
from __future__ import annotations
import math
from python_ta.contracts import check_contracts

###############################################################################
# The two building blocks: AirlineGraph, _AirportVertex


# @check_contracts
class AirlineGraph:
    """A class representing the graph of the airports.

    Representation Invariants:
        - all(len(code) == 3 or 4 for code in self._airports)
    """
    # Private Instance Attributes:
    # - _airports: a dictionary of the airports vertices contained in this graph. Maps the name(IATA code) of the
    # airports to _AirportVertex.
    _airports: dict[str, _AirportVertex]

    def __init__(self) -> None:
        """Initialize an empty AirlineGraph (no vertices or edges).
        """
        self._airports = {}

    def add_airport_vertex(self, airport: str, position: tuple[float, float],
                           country: str = 'Canada', province: str = None) -> None:
        """Add a new airport_vertex with the given item to this graph.

        The new airport_vertex is not adjacent to any other vertices.

        Preconditions:
            - airport not in self._airports

        >>> graph = AirlineGraph()
        >>> graph.add_airport_vertex('YYZ', (43.67720032, -79.63059998), 'Canada', 'ON')
        >>> 'YYZ' in graph._airports
        True
        """
        if airport not in self._airports:
            self._airports[airport] = _AirportVertex(name=airport,
                                                     position=position,
                                                     country=country,
                                                     province=province)

    def add_route(self, airport1: str, airport2: str, airline_num: int = 1) -> None:
        """Add a route between the two airport vertices with the given items in this graph.

        Additionally, the airline number is also added to the value of the dictionary corresponding to the airport key.

        Raise a ValueError if airport1 or airport2 do not appear as vertices in this airline graph.

        Preconditions:
            - (airport1 in self._airports) and (airport2 in self._airports)
            - airport1 != airport2

        >>> graph = AirlineGraph()
        >>> graph.add_airport_vertex('YYZ', (43.67720032 ,-79.63059998), 'Canada', 'ON')
        >>> graph.add_airport_vertex('YVR', (49.19390106 ,-123.1839981), 'Canada', 'BC')
        >>> graph.add_route('YYZ', 'YVR', 1)
        >>> graph.adjacent('YYZ', 'YVR')
        True
        """
        if airport1 in self._airports and airport2 in self._airports:
            a1 = self._airports[airport1]
            a2 = self._airports[airport2]

            if a2 not in a1.neighbours:
                a1.neighbours[a2] = airline_num
            else:
                a1.neighbours[a2] += airline_num

            if a1 not in a2.neighbours:
                a2.neighbours[a1] = airline_num
            else:
                a2.neighbours[a1] += airline_num

        else:
            raise ValueError

    def adjacent(self, airport1: str, airport2: str) -> bool:
        """Return whether airport1 or airport2 are adjacent airport vertices in this airline graph.

        Also return False if airport1 or airport2 do not appear as airport vertices in this airline graph.
        """
        if airport1 in self._airports and airport2 in self._airports:
            a1 = self._airports[airport1]
            return any(a2.name == airport2 for a2 in a1.neighbours.keys())
        else:
            return False

    def get_neighbours(self, airport: str) -> set:
        """Return a set of neighbours of the given airport, according to their names(IATA code).

        Preconditions:
            - airport in self._airports

        >>> graph = AirlineGraph()
        >>> graph.add_airport_vertex('YYZ', (43.67720032 ,-79.63059998), 'Canada', 'ON')
        >>> graph.add_airport_vertex('YVR', (49.19390106 ,-123.1839981), 'Canada', 'BC')
        >>> graph.add_route('YYZ', 'YVR', 1)
        >>> graph.get_neighbours('YYZ')
        {'YVR'}
        """
        if airport in self._airports:
            a = self._airports[airport]
            return {n.name for n in a.neighbours}
        else:
            raise ValueError

    def connected(self, airport1: str, airport2: str) -> bool:
        """Return whether airport1 or airport2 are connected airport vertices in this airline graph.

        Return False if airport1 or airport2 do not appear as airport vertices in this airline graph.

        Preconditions:
            - (airport1 in self._airports) and (airport2 in self._airports)

        >>> graph = AirlineGraph()
        >>> graph.add_airport_vertex('YYZ', (43.67720032 ,-79.63059998), 'Canada', 'ON')
        >>> graph.add_airport_vertex('YVR', (49.19390106 ,-123.1839981), 'Canada', 'BC')
        >>> graph.add_airport_vertex('YUL', (45.47060013 ,-73.74079895), 'Canada', 'QC')
        >>> graph.add_route('YYZ', 'YVR', 1)
        >>> graph.add_route('YYZ', 'YUL', 1)
        >>> graph.connected('YVR', 'YUL')
        True
        """
        if airport1 in self._airports and airport2 in self._airports:
            a1 = self._airports[airport1]
            return a1.check_connected(airport2, set())
        else:
            return False

    def find_shortest_path(self, start: str, end: str) -> list[_AirportVertex]:
        """find the shortest path between the two airport, if there is a tie, return the first that appears.
        """
        all_paths = self.find_paths(start, end)
        smallest = all_paths[0]
        smallest_distance = self.calculate_paths_distance(smallest)

        for i in range(1, len(all_paths)):
            curr = all_paths[i]
            curr_distance = self.calculate_paths_distance(curr)
            if smallest_distance > curr_distance:
                smallest = curr
                smallest_distance = curr_distance

        return smallest

    def find_paths(self, start: str, end: str) -> list[list[_AirportVertex]]:
        """Return a list of all possible paths from this vertex that do NOT use any aiports in visited.
        """
        start = self._airports[start]
        destination = self._airports[end]
        return start.find_paths(destination, set())

    def calculate_paths_distance(self, paths: list[_AirportVertex]) -> float:
        """calculate the distance of the total paths from the first airport to the last airport based on longitude and
        latitude.
        """
        accu = 0.0
        for i in range(1, len(paths) - 1):
            accu += self.get_distance(paths[i - 1].name, paths[i].name)
        return accu

    def get_distance(self, airport1: str, airport2: str) -> float:
        """Return the distance between airport1 and airport2 based on their longitude and latitude recorded in their
        own vertices

        Preconditions:
            - (airport1 in self._airports) and (airport2 in self._airports)

        >>> graph = AirlineGraph()
        >>> graph.add_airport_vertex('YYZ', (43.67720032 ,-79.63059998), 'Canada', 'ON')
        >>> graph.add_airport_vertex('YVR', (49.19390106 ,-123.1839981), 'Canada', 'BC')
        >>> round(graph.get_distance('YYZ', 'YVR'), 4)
        3346.5625
        """
        if airport1 in self._airports and airport2 in self._airports:
            a1 = self._airports[airport1]
            a2 = self._airports[airport2]
            lat1 = math.radians(a1.position[0])
            lat2 = math.radians(a2.position[0])
            lon1 = math.radians(a1.position[1])
            lon2 = math.radians(a2.position[1])
            diff_lat = abs(lat1 - lat2)
            diff_lon = abs(lon1 - lon2)
            a = math.sin(diff_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return 6373.0 * c
        else:
            raise ValueError

    def get_airports_within_diameter(self, airport: str, d: float) -> set:
        """Return a set of airports that is within the diameter compared to the given airport, according to their
        names(IATA code)

        Preconditions:
            - airport in self._airports

        >>> graph = AirlineGraph()
        >>> graph.add_airport_vertex('YYZ', (43.67720032 ,-79.63059998), 'Canada', 'ON')
        >>> graph.add_airport_vertex('YVR', (49.19390106 ,-123.1839981), 'Canada', 'BC')
        >>> graph.get_airports_within_diameter('YYZ', 3500.0)
        {'YVR'}
        """
        if airport in self._airports:
            s = set()
            for air in self._airports.values():
                if self.get_distance(airport, air.name) <= d:
                    s.add(air.name)
            s.remove(airport)
            return s
        else:
            raise ValueError

    def get_airport_vertices(self) -> list[_AirportVertex]:
        """Return all the airport vertices in this airline graph.

        """
        return list(self._airports.values())

    def get_airports(self) -> list[str]:
        """Return all the airport names(in IATA code) in this airline graph.

        """
        return list(self._airports)

    def calculate_total_airlines(self, airport: str) -> int:
        """Return the total numbers of airlines that n airport has in this graph.

        Precondition:
            - airport in self._airports

        >>> graph = AirlineGraph()
        >>> graph.add_airport_vertex('YYZ', (43.67720032 ,-79.63059998), 'Canada', 'ON')
        >>> graph.add_airport_vertex('YVR', (49.19390106 ,-123.1839981), 'Canada', 'BC')
        >>> graph.add_route('YYZ', 'YVR', 1)
        >>> graph.calculate_total_airlines('YYZ')
        1
        """
        air_vertex = self._airports[airport]
        num = air_vertex.calculate_total_airlines()

        return num


# @check_contracts
class _AirportVertex:
    """A vertex of the airport in the graph.

        Instance Attributes:
        - name: the IATA code of the airport vertex.
        - position: the position of the airline in this airport vertex, marked as (latitude, longitude).
        - country: the country of the airport vertex location.
        - province: the province of the airport vertex location.
        - neighbours: The vertices that are adjacent to this airport vertex.

    Representation Invariants:
        - len(self.name) == 3 or 4
        - airline_num >= 0
        - len(province) == 2
        - all(self.check_connected(neighbour.name) for neighbour in self.neighbours)
    """
    name: str
    position: tuple[float, float]
    country: str
    province: str | None
    neighbours: dict[_AirportVertex, int | None]

    def __init__(self, name: str, position: tuple[float, float], country: str = 'Canada', province: str = None) -> None:
        """Initialize a new _AirportVertex with the given name, position, airport_size, province.
        """
        self.name = name
        self.position = position
        self.country = country
        self.province = province
        self.neighbours = {}

    def check_connected(self, target_name: str, visited: set[_AirportVertex]) -> bool:
        """Return whether this _AirportVertex is connected to a _AirportVertex corresponding to the target_name,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """
        if self.name == target_name:
            # Our base case: the target_item is the current vertex
            return True
        else:
            visited.add(self)        # Add self to the list of visited vertices
            for u in self.neighbours:
                if u not in visited and u.check_connected(target_name, visited):
                    # Only recurse on vertices that haven't been visited
                    return True

            return False

    def calculate_total_airlines(self) -> int:
        """Return the total numbers of airlines that this airline vertex has.
        """
        num = 0

        for i in self.neighbours.values():
            num += i

        return num

    ###############################################################################################
    # Computing all paths
    ###############################################################################################
    def find_paths(self, destination: _AirportVertex, visited: set[_AirportVertex]) -> list[list[_AirportVertex]]:
        """Return all possible paths from self to a destination airport vertex.
        """
        if self == destination:
            return [[self]]

        paths_tot = []
        visited.add(self)
        for neighbour_vertex in self.neighbours:
            if neighbour_vertex not in visited:
                neighbour_paths = neighbour_vertex.find_paths(destination, visited)

                for path in neighbour_paths:
                    paths_tot.append([self] + path)

        return paths_tot


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['math'],
        'max-line-length': 120,
        'disable': ['unused-import']
    })
