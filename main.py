"""CSC111 Winter 2023 Project: World Aircraft Routes

Instructions
===============================

This Python module contains a collection of Python classes and functions that is
used in visualize airports and aircraft routes on real world map.

Copyright and Usage Information
===============================

This file is a part of the project used in CSC111 at the University of Toronto
St. George campus.

This file is copyright (c) 2023 Qixuan Chu, Xuanjun Dong, Meizhou Su, Siyu Wu
"""
import webbrowser
import data_collection
import visualization


def runner(region: str, departure: str, destination: str) -> None:
    """This function would plot two graphs.

    The first graph visualizes the airports and aircraft routes based on selected region on real world map.

    The second graph visualizes the best paths from departure airport to destination airport based on selected airports
    (in IATA code).

    Tips: It may take few seconds to have the worldwide aircraft routes. Please wait patiently.

    Preconditions:
        - region is one of the country in the world with first letter capitalized or 'World'
        - departure and destination are the IATA codes of the airports in the selected region.
        - len(departure) == 3 or 4
        - len(departure) == 3 or 4
    """
    if region == 'World':
        airline_graph = data_collection.load_airport_file_global('data/airports.csv')
        data_collection.load_route_file('data/routes.csv', airline_graph)
        visualization.plot_graph_world(airline_graph)
    elif region == 'Canada':
        airline_graph = data_collection.load_airport_file_ca('data/ca-airports.csv')
        data_collection.load_route_file('data/routes.csv', airline_graph)
        visualization.plot_graph_country(airline_graph, 'Canada')
    else:
        airline_graph = data_collection.load_airport_file_global('data/airports.csv')
        data_collection.load_route_file('data/routes.csv', airline_graph)
        visualization.plot_graph_country(airline_graph, region)

    shortest_paths = airline_graph.find_shortest_path(departure, destination)
    visualization.plot_shortest_paths(shortest_paths)


def runner_interactive() -> None:
    """This function is an interactive function.

    It firstly asks user to choose the region you would like to visualize the airports and aircraft routes.

    Then it helps generate the kml file that can be imported on Google Earth in /data/ folder based on selected region.

    And it would ask the user's willingness to open the Google Earth website.

    Lastly, it visualizes the best paths from departure airport to destination airport based on user's choices.

    Tips: It may take few seconds to have the worldwide aircraft routes and the kml file. Please wait patiently.

    """
    default = input('Do you want to run with default mode (Canada)?\nPlease answer with yes or no:')
    print('Your answer is: ' + default + '\n\n')
    if default == 'yes':
        choice = 'Canada'
        airline_graph = data_collection.load_airport_file_ca('data/ca-airports.csv')
        data_collection.load_route_file('data/routes.csv', airline_graph)
        visualization.plot_graph_country(airline_graph, 'Canada')
    else:
        choice = input('Please enter country name with first letter capitalized '
                       'or enter "World" if you want to see Global routes')
        print('You selected ' + choice+ '\n\n')

        if choice == 'World':
            airline_graph = data_collection.load_airport_file_global('data/airports.csv')
            data_collection.load_route_file('data/routes.csv', airline_graph)
            visualization.plot_graph_world(airline_graph)
        else:
            airline_graph = data_collection.load_airport_file_global('data/airports.csv')
            data_collection.load_route_file('data/routes.csv', airline_graph)
            visualization.plot_graph_country(airline_graph, choice)

    print('We have drawn a graph based on your choice.\n\n'
          'If no graph is shown, please check if you entered a valid country name.\n\n'
          '\nAdditionally, we can created a kml file that can be imported on Google Earth in \'data\' folder '
          'based on your choice')

    web = input('\nPlease enter Y if you would like to create the kml file and open the Google Earth.\n'
                'Otherwise you would be asked to find '
                'the shortest path between two different airports you want.')

    if web == 'Y':
        if choice == 'World':
            visualization.output_graph_world(airline_graph)
        else:
            visualization.output_graph_country(airline_graph, choice)

        webbrowser.open_new_tab('https://earth.google.com/web/')

    print('\nNow I can help you find the shortest path between two different airports you want on the worldwide map')
    departure = input('\nPlease enter the place of departure with IATA code: ')
    destination = input('\nPlease enter the place of destination with IATA code: ')

    shortest_paths = airline_graph.find_shortest_path(departure, destination)
    visualization.plot_shortest_paths(shortest_paths)

    print('The best paths have been shown.\nThanks for your cooperation. This function has ended!')


if __name__ == '__main__':
    # Sample call to part_runner which visualizes the airports and aircraft routes in Canada,
    # and visualizes the best paths from YYZ to YVP (you can change this, just keep it in the main block!)
    runner('Canada', 'YYZ', 'YVP')

    # You may also comment out the runner_interactive function in the main block to run the code in an interactive way.

    # runner_interactive()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['data_collection', 'visualization', 'webbrowser', 'plotly.graph_objects'],
        'max-line-length': 120,
        'allowed-io': ['runner', 'runner_interactive'],
        'disable': ['unused-import']
    })
