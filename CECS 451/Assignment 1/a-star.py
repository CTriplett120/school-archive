import sys
import math


def distance_between(start, end):
    """
    Finds the distance between two points. Points must be passed in as tuples of (latitude, longitude)
    """

    lat1 = start[0] * math.pi/180
    long1 = start[1] * math.pi/180
    lat2 = end[0] * math.pi / 180
    long2 = end[1] * math.pi / 180

    x1 = math.sin((lat2 - lat1) / 2) ** 2
    x2 = math.cos(lat1) * math.cos(lat2) * (math.sin((long2 - long1) / 2) ** 2)

    y = math.sqrt(x1 + x2)

    return 2 * 3958.8 * math.asin(y)


def main():
    if len(sys.argv) < 3:
        raise AssertionError("Two arguments should be provided")
    start_city = sys.argv[1]
    end_city = sys.argv[2]

    # ensure that the two cities are actually different
    if start_city == end_city:
        raise AssertionError("Cites must be different")

    # copy coordinates.txt into a dictionary
    with open("coordinates.txt") as coordinates:
        coords = {}
        data = coordinates.read().split('\n')
        for entry in data:
            entry = entry.split(':')

            lat, lon = entry[1].strip('()').split(',')

            coords[entry[0]] = (float(lat), float(lon))

    # copy map.txt into a dictionary
    with open("map.txt") as cali_map:
        connections = {}
        data = cali_map.read().split('\n')
        for entry in data:
            entry = entry.split('-')
            lines = entry[1].split(',')
            structured_lines = []
            for line in lines:
                x = line.split('(')
                line = (x[0], float(x[1].strip(')')))
                structured_lines.append(line)

            connections[entry[0]] = structured_lines

    # ensure that both cities are in both files
    try:
        coords[start_city]
        coords[end_city]
        connections[start_city]
        connections[end_city]
    except KeyError:
        raise KeyError("One or both input cities is unknown")

    # a route is stored as a tuple of (city name, path (city1 - city2 - ... - end), route distance)
    routes = []

    # used for sorting routes
    def key_function(item):
        return item[2] + distance_between(coords[item[0]], coords[end_city])

    # a* algorithm

    selected_node = (start_city, f"{start_city}", 0.0)  # starting place

    # while path to end_city has not been found
    while selected_node[0] != end_city:

        # scan neighbors of selected node and add them to nodes
        for link in connections[selected_node[0]]:
            prospective_route = (link[0], f"{selected_node[1]} - {link[0]}", selected_node[2] + link[1])

            # prevent backtracking/cycles
            city_list = prospective_route[1].split(' - ')
            if len(city_list) == len(set(city_list)):  # checks for duplicate cities (city1 - city2 - city1)
                routes.append(prospective_route)

        # sort routes to find best one
        routes.sort(key=key_function)

        # explore the best potential route
        selected_node = routes.pop(0)

    # output statement
    print(f"From city: {start_city}\nTo city: {end_city}\nBest Route: {selected_node[1]}\nTotal distance: {selected_node[2]}")


if __name__ == "__main__":
    main()
