# Main entry point for the program
# Also contains logic for the optimized process of loading and delivering packages
# Name: Steven Kazmierkiewicz
# Student ID: 001367934

import cli
import delivering
import dijkstras
import issues
from models.package import Package
from models.truck import Truck
from datetime import time
import csv_parsing.location_csv as location_csv
import csv_parsing.package_csv as package_csv
import loading


if __name__ == '__main__':
    truck1 = Truck(1, time(8), loading.HUB_ADDRESS)
    truck2 = Truck(2, time(8), loading.HUB_ADDRESS)

    location_hash = location_csv.read()  # O(n^3)
    graph = dijkstras.build_graph(location_hash)  # O(n^3)
    package_hash, priority_1, priority_2, priority_3, delayed, sibling_sets = package_csv.read()  # O(n^3)

    # Initial Loading

    # -- Load sibling sets
    loading.load_siblings_dijkstras([truck1, truck2], sibling_sets, [priority_1, priority_2, priority_3], package_hash)  # O(n^3)

    # -- Sort Trucks
    loading.sort_truck_dijkstras(truck1, graph, package_hash)  # O(n^3)
    loading.sort_truck_dijkstras(truck2, graph, package_hash)  # O(n^3)
    # -- Main loading
    loading.initiate_loading_dijkstras([truck1, truck2], [priority_1, priority_2, priority_3], graph, package_hash)  # O(n^6)

    # -- Deliver first round
    while not truck1.empty():  # O(n^2)
        delivering.deliver_dijkstras(truck1, package_hash)   # O(n)

    while not truck2.empty():  # O(n^2)
        delivering.deliver_dijkstras(truck2, package_hash)  # O(n)

    # Trucks return to hub
    delivering.return_to_hub([truck1, truck2], loading.HUB_ADDRESS, location_hash)  # O(n^2)

    # Repeat until there are no more package
    while len(delayed + priority_1 + priority_2 + priority_3) > 0:  # O(n^7)

        # First truck done will load and deliver immediately
        [first_truck, last_truck] = loading.get_return_order_of_trucks([truck1, truck2])  # O(n^2)

        # Check for fixing wrong address and delayed package issues
        issues.check_issues(first_truck.time, delayed,
                            {
                                Package.PRIORITY_1: priority_1,
                                Package.PRIORITY_2: priority_2,
                                Package.PRIORITY_3: priority_3
                            }, package_hash)  # O(n^2)

        # Load first truck
        loading.initiate_loading_dijkstras([first_truck], [priority_1, priority_2, priority_3], graph, package_hash)  # O(n^6)

        # Deliver first truck that returned to hub
        while not first_truck.empty():  # O(n^2)
            delivering.deliver_dijkstras(first_truck, package_hash)  # O(n)

        # Return to the hub
        delivering.return_to_hub([first_truck], loading.HUB_ADDRESS, location_hash)  # O(n^2)

        # Second truck done will wait for last delayed package, if any
        # Need to find the time of last delayed package and set
        # the second truck's time to this.
        # There should be no delayed packages after the first iteration.
        if len(delayed) > 0:
            last_delayed_pkg = loading.get_last_delayed_package(delayed, package_hash)  # O(n^2)
            last_truck.time = last_delayed_pkg.delay_time

        # Check for fixing wrong address and delayed package issues
        issues.check_issues(last_truck.time, delayed,
                            {
                                Package.PRIORITY_1: priority_1,
                                Package.PRIORITY_2: priority_2,
                                Package.PRIORITY_3: priority_3
                             },
                            package_hash)  # O(n^2)

        # If first truck returns before second truck leaves, first truck must wait at least until second truck
        # leaves before loading again.
        if first_truck.time < last_truck.time:
            first_truck.time = last_truck.time

        # Load second truck
        loading.initiate_loading_dijkstras([last_truck], [priority_1, priority_2, priority_3], graph, package_hash)  # O(n^6)

        # Deliver second truck
        while not last_truck.empty():  # O(n^2)
            delivering.deliver_dijkstras(last_truck, package_hash)  # O(n)

        # Return to the hub
        delivering.return_to_hub([last_truck], loading.HUB_ADDRESS, location_hash)  # O(n^2)

    # Print length of buckets in package hash
    # for i in range(len(package_hash.table)):
    #     print(str(i) + ': ' + str(len(package_hash.table[i])) + ' packages')

    # Give control of the program to the command line interface for user input
    cli.control([truck1, truck2], [delayed, priority_1, priority_2, priority_3], package_hash)













