"""CSC111 Winter 2023 Project: World Aircraft Routes

Instructions
===============================

This Python module contains a collection of Python functions that is used for
visualizing airports and aircraft routes on real world map.

Copyright and Usage Information
===============================

This file is a part of the project used in CSC111 at the University of Toronto
St. George campus.

This file is copyright (c) 2023 Qixuan Chu, Xuanjun Dong, Meizhou Su, Siyu Wu
"""
import simplekml
import plotly.graph_objects as go
from airline_graph import _AirportVertex
from airline_graph import AirlineGraph


def output_graph_world(airlines: AirlineGraph) -> None:
    """A function that generates the worldwide AirlineGraph into kml file which can be imported into Google Earth.
    """
    kml = simplekml.Kml()
    visited = set()

    for airport in airlines.get_airport_vertices():
        visited.add(airport.name)
        lat, lon = airport.position

        kml.newpoint(name=airport.name, coords=[(lon, lat)])

        for neighbour in airport.neighbours:
            if neighbour.name not in visited:
                neighbour_lat, neighbour_lon = neighbour.position
                kml.newlinestring(name=airport.name + ' to ' + neighbour.name,
                                  coords=[(lon, lat), (neighbour_lon, neighbour_lat)])

        kml.save('data/world_airlines.kml')


def output_graph_country(airlines: AirlineGraph, choice: str = 'Canada') -> None:
    """A function that generates the AirlineGraph in any conutry in the world into kml file which can be imported into
    Google Earth.

    Preconditions:
        - Choice is one of the country in the world with first letter capitalized
    """
    kml = simplekml.Kml()
    visited = set()

    for airport in airlines.get_airport_vertices():
        visited.add(airport.name)
        if airport.country == choice:
            lat, lon = airport.position

            kml.newpoint(name=airport.name, coords=[(lon, lat)])

            for neighbour in airport.neighbours:
                if neighbour.name not in visited and neighbour.country == choice:
                    neighbour_lat, neighbour_lon = neighbour.position
                    kml.newlinestring(name=airport.name + ' to ' + neighbour.name,
                                      coords=[(lon, lat), (neighbour_lon, neighbour_lat)])

    kml.save('data/' + choice + '_airlines.kml')


def plot_graph_world(airlines: AirlineGraph) -> None:
    """plot a graph of the airports and routes by plotly from a complete Airline graph.
    """
    fig = go.Figure()
    visited = set()

    for airport in airlines.get_airport_vertices():
        visited.add(airport.name)
        lon = airport.position[1]
        lat = airport.position[0]
        fig.add_trace(go.Scattergeo(
            lon=[lon],
            lat=[lat],
            hoverinfo='text',
            text=airport.name,
            mode='markers',
            marker=dict(
                size=2,
                color='rgb(255, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

        for neighbour in airport.neighbours:
            if neighbour.name not in visited:
                neighbour_lat, neighbour_lon = neighbour.position

                fig.add_trace(
                    go.Scattergeo(
                        lon=[lon, neighbour_lon],
                        lat=[lat, neighbour_lat],
                        mode='lines',
                        text=airport.name + ' - ' + neighbour.name,
                        line=dict(width=1, color='blue')
                    )
                )

    title_text = 'World Aircraft Routes'
    scope = 'world'

    fig.update_layout(
        title_text=title_text,
        showlegend=False,
        geo=dict(
            scope=scope,
            projection_type='azimuthal equal area',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
    )

    fig.show()


def plot_graph_country(airlines: AirlineGraph, choice: str = 'Canada') -> None:
    """plot a graph of the airports and routes by plotly from a complete Airline graph.

    Preconditions:
        - Choice is one of the country in the world with first letter capitalized
    """
    fig = go.Figure()
    visited = set()

    for airport in airlines.get_airport_vertices():
        visited.add(airport.name)
        if airport.country == choice:
            lon = airport.position[1]
            lat = airport.position[0]
            fig.add_trace(go.Scattergeo(
                lon=[lon],
                lat=[lat],
                hoverinfo='text',
                text=airport.name + str(lon) + str(lat),
                mode='markers',
                marker=dict(
                    size=2,
                    color='rgb(255, 0, 0)',
                    line=dict(
                        width=3,
                        color='rgba(68, 68, 68, 0)'
                    )
                )))

            for neighbour in airport.neighbours:
                if neighbour.name not in visited and neighbour.country == choice:
                    neighbour_lat, neighbour_lon = neighbour.position

                    fig.add_trace(
                        go.Scattergeo(
                            lon=[lon, neighbour_lon],
                            lat=[lat, neighbour_lat],
                            mode='lines',
                            text=airport.name + ' - ' + neighbour.name,
                            line=dict(width=1, color='blue')
                        )
                    )

    if choice == 'Canada':
        title_text = 'Canada Aircraft Routes'
        scope = 'north america'
    else:
        title_text = choice + ' Aircraft Routes'
        scope = 'world'
    fig.update_layout(
        title_text=title_text,
        showlegend=False,
        geo=dict(
            scope=scope,
            projection_type='azimuthal equal area',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
    )

    fig.show()


def plot_shortest_paths(paths: list[_AirportVertex]) -> None:
    """plot the shortest paths from the departure to the destination on worldwide real map

    Preconditions:
        - len(paths) >= 2
    """
    fig = go.Figure()

    for i in range(1, len(paths)):
        lon_1 = paths[i - 1].position[1]
        lon_2 = paths[i].position[1]
        lat_1 = paths[i - 1].position[0]
        lat_2 = paths[i].position[0]
        fig.add_trace(
            go.Scattergeo(
                lon=[lon_1, lon_2],
                lat=[lat_1, lat_2],
                mode='lines',
                text=paths[i - 1].name + ' - ' + paths[i].name,
                line=dict(width=1, color='red')
            )
        )

    fig.update_layout(
        title_text='best paths from ' + paths[0].name + ' to ' + paths[-1].name,
        showlegend=False,
        geo=dict(
            scope='world',
            projection_type='azimuthal equal area',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
    )

    fig.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['simplekml', 'plotly.graph_objects', 'airline_graph'],
        'max-line-length': 120,
        'allowed-io': ['output_graph', 'plot_graph', 'plot_shortest_paths'],
        'disable': ['unused-import', 'too-many-nested-blocks']
    })
