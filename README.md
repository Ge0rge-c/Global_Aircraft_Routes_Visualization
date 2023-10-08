# Introduction of Project

Airports serve as important transportation hubs that connect countries and international destinations across the
world, making it easier for people to work, study and travel. However, due to the differences in development,
economic level, topography, population and other aspects of each country, airport routes and city traffic conditions
are different.

To better understand global transportation and urban development, we would like to create a visual map
of airport routes and city traffic in recent years for each country in the world. This project demonstrates the routes
between airports around the world, as well as how these airports are distributed.

This project can provide people with a visual and useful tool to help them better understand transportation and
urban development in different countries. Through the visualization of this project, people can clearly observe the
connections between countries in the world by air traffic, which allows clients to compare the routes between countries
and their cities, and thus better understand the level of development of the aviation industry in different countries.
Moreover, this project can be used to understand transportation links and population density between countries and
cities, to identify needs for transportation infrastructure development. Also, tourism practitioners can use
this project to understand the distribution of airports and routes in different regions to inform tourism planning.
In summary, the goal of our project is to implement the airport routes visual map of the world or
any country that can provide a more comprehensive tool for understanding air traffic and urban
development around the world and provide in-need information and reference for tourism planning
or other uses.

# Used Datasets

We mainly use three data sets in our project.
• ca-airports.csv
This file contains the basic information of each airport in Canada. It downloads from
https://data.humdata.org/dataset/ourairports-can?force layout=desktop.
The columns we used are ’iata code’, ’latitude deg’, ’longitude deg’, ’country name’ and ’local region’.

• airports.csv
This file contains airports information all over the world. It downloads from
https://data.world/tylerudite/airports-airlines-and-routes
The columns ’latitude deg’, ’longitude deg’, ’country name’, ’local region’, and ’iata code’ are actually used.

• routes.csv
This file includes all routes around the world. We only use ’Source airport’ and ’Destination airports’ for this
data set. It downloads from
https://data.world/tylerudite/airports-airlines-and-routes
For this file, the used columns are ’Source airport’ and ’Destination airport’.

# Computational Overview

For this project, we use Graph to model our central data. First, we construct a private class called AirportVertex
as the base Vertex for our Graph, where the attributes contain name:str (the IATA code of the airport vertex, e.g.
YYZ), position:tuple[float](the position of the airline in this airport vertex, marked as (latitude, longitude)),
country:str(the country of the airport vertex location), province:str(the province of the airport vertex location),
and neighbours:dict[Airport, int|None]. For neighbours attribute, the key is the AirportVertex adjacent to
the airport (we define ”adjacent” to mean that there are direct flights between the two airports), and the value
is the number of direct flights between the two airports. Then we use the AirportVertex to build a class called
AirlineGraph, which is the main Graph data structure we use. This graph class only has one private instance
attribute which is airports:dict[str, AirportVertex], the key is the IATA code of the airport vertex and the
value is the AirportVertex corresponding to the IATA code.

Using a graph as the core data type for representing world airports and routes is a powerful structure that can
bring a lot of convenience. The graph provides a natural and intuitive way to represent the structure of the airport
system, where the airports are represented as vertices and the routes as edges. This allows for easy visualization
and understanding of the relationships between airports and routes. In addition, Using the vertices of the graph to
represent the airports can list the basic information of the airports clearly. We can perform the desired analysis tasks
accordingly. For example, in airline graph.py, we implemented the check connected method in AirportVertex
to check if there is a path between two airports. And we are able to implement some iterative algorithms we want
more easily by building graphs. Like in airline graph.py we build the find path method that we use to find the
shortest path between two airports using an iterative algorithm. In addition, graph structure can help us to handle
large amounts of data to build the structure of airports and routes. Such as the three functions in data collection.py
use the add airport vertex and add route methods in AirlineGraph to process the data and add airports and
routes to the graph to build our structure.

Since the goal we want to achieve is to display all the information we integrate on a map of Canada and other
countries in the world, the Plotly library is the first choice for us. In the visualization.py file, we implement
plot graph country and plot graph world function by using functions of Plotly library. These two functions are
used for the visualization of our maps. We mainly use the add trace function of Plotly to record airports and
routes as points and lines on our plotted maps. After this function is executed, the drawn map page will pop up
automatically. The red dots represent the airports and the blue lines represent the routes.
It is worth mentioning that we also provide another option for the clients to view the map, which is to import the air-
ports and routes kml file to Google Earth website. In the visualization.py file, we implement output graph country
and output graph world function to generate a kml file about airports and routes by inputting the AirlineGraph.
In these two functions we mainly use functions from the simplekml library to record airports and routes as points
and lines in the kml file, by using the latitude and longitude of the airports in the AirlineGraph. newpoint func-
tion is used to record points and newlinestring function is used to record lines. The generated kml file will be
automatically saved in the data folder we provide, then clients need to manually import the generated kml file into
Google Earth website to see it, which is pretty cool. This way is more intuitive and clearer than plotly, and with
the advantage of Google Earth you can observe more details of the map.

No matter which visualization method the clients choose, there is no difference in the core we want to show, but
we hope that they can have a better experience with our project from different views and in different ways. Both of
our methods offer the option of generating maps for the world or any country, so users can choose according to their
needs. If clients are interested in observing the worldwide routes, they should try to generate global routes, which is
stunning. We prefer to suggest clients try the method of importing kml files to implement it, since due to the large
dataset, the lag delay of the map generated by Plotly may be more serious.

# References
“Airports in Canada.” Humanitarian Data Exchange,
https://data.humdata.org/dataset/ourairports-can?force layout=desktop.

“Airports, Airlines, and Routes.” Data.world, 6 June 2022,
https://data.world/tylerudite/airports-airlines-and-routes

“Maps.” Maps in Python,
https://plotly.com/python/maps/.

”Lines.” Lines on mapbox in Python. (n.d.). Retrieved April 4, 2023,
https://plotly.com/python/lines-on-mapbox/

”Simplekml.” PyPI. (n.d.). Retrieved April 4, 2023,
https://pypi.org/project/simplekml/

”Python custom KML points, lines, polygons, circles.” YouTube. Retrieved April 4, 2023,
https://www.youtube.com/watch?v=NJ5eG-hmdTE



