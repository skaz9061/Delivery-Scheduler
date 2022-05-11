# Module for delivering packages

import utils


def deliver(truck, package_hash, location_hash):
    """
    .. warning:: USED IN A PREVIOUS VERSION. NOT CURRENTLY USED. Use **deliver_dijkstras** instead.

    Delivers the next package off of the truck and updates the state of the truck and package objects.

    :param Truck truck: the delivering truck
    :param ChainingHashTable[str, Package] package_hash: Package objects
    :param ChainingHashTable[str, Location] location_hash: Location objects
    :return:
    """
    # O(n) because of ChainingHashTable.lookup
    pkg_id = truck.deliver()
    pkg = package_hash.lookup(pkg_id)
    distance = location_hash.lookup(truck.current_address).get_distance(pkg.address)
    hours = float(distance) / float(truck.SPEED)
    eta = utils.add_time(truck.time, utils.timedelta(hours=hours))

    # Update the truck
    truck.distance += distance
    truck.time = eta
    truck.current_address = pkg.address

    # Update the package
    pkg.advance_status(eta, truck.id)


def deliver_dijkstras(truck, package_hash):
    """
    Delivers the next package off of the truck and updates the state of the truck and package objects.

    *This version uses Dijkstra's Algorithm.*

    :param Truck truck: the delivering truck
    :param ChainingHashTable[str, Package] package_hash: Package objects
    :return:
    """
    # Time complexity O(n)
    pkg_id, distance = truck.deliver()
    pkg = package_hash.lookup(pkg_id)  # O(n)
    hours = float(distance) / float(truck.SPEED)
    eta = utils.add_time(truck.time, utils.timedelta(hours=hours))

    # Update the truck
    truck.distance += distance
    truck.time = eta
    truck.current_address = pkg.address

    # Update the package
    pkg.advance_status(eta, truck.id)


def return_to_hub(truck_list, hub, location_hash):
    """
    Returns all the trucks provided to the hub and updates their address, time, and distance traveled.

    :param list[Truck] truck_list: (list) the Truck objects
    :param str hub: address of the hub
    :param ChainingHashTable[str, Location] location_hash: the Location objects
    :return:
    """
    # Time complexity O(n^2)
    for truck in truck_list:
        distance_to_hub = location_hash.lookup(truck.current_address).get_distance(hub)  # O(n)
        truck.distance += distance_to_hub
        truck.time = utils.add_time(truck.time, utils.timedelta(hours=distance_to_hub/truck.SPEED))
        truck.current_address = hub
