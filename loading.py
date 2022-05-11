# Module for loading packages onto the truck and associated methods
import dijkstras

HUB_ADDRESS = '4001 South 700 East'


def load_package_dijkstras(truck, pkg_id_list, g, package_hash):
    """
    Loads the next package onto a truck.

    Nearest neighbor of the previous package added onto the truck is used to find the next package. If the truck is
    empty, then the nearest neighbor of the Hub is used.

    *This version uses Dijkstra's Algorithm.*

    :param Truck truck: the truck being loaded
    :param list[str] pkg_id_list: the list of package ids currently being loaded from
    :param Graph g: the Graph structure that Dijkstra's Algorithm has been run on
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return: True if a package was found to load onto the truck, False if no package was available to be loaded
    """
    # Time complexity O(n^2)
    if not truck.full() and len(pkg_id_list) > 0:
        if truck.last_package_dijkstras() == -1:
            truck_add = HUB_ADDRESS
        else:
            truck_add = package_hash.lookup(truck.last_package_dijkstras()).address  # O(n)

        next_pkg_id, next_pkg_distance = find_closest_pkg_dijkstras(truck_add, truck.id, pkg_id_list, g, package_hash)  # O(n^2)

        next_pkg = package_hash.lookup(next_pkg_id)  # O(n)

        if not next_pkg:
            return False
        else:
            truck.add_package_dijkstras(next_pkg_id, next_pkg_distance)
            package_hash.lookup(next_pkg_id).advance_status(truck.time, truck.id)  # O(n)
            pkg_id_list.remove(next_pkg_id)  # O(n)
            return True


def find_closest_pkg_dijkstras(curr_add, truck_id, pkg_id_list, g, package_hash):
    """
    Finds the nearest package destination to the current address that is allowed on the specific truck.

    *This version uses Dijkstra's Algorithm.*

    :param str curr_add: the current address
    :param int truck_id: the id of the current truck
    :param list[str] pkg_id_list: the package ids currently being loaded
    :param Graph g: the Graph structure that Dijkstra's Algorithm has been run on
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return: the id of the closest package destination, '-1' if none found
    :rtype: str
    """
    # Time complexity O(n^2)
    min_pkg_id = '-1'
    min_pkg_distance = float('inf')

    g.reset()  # O(n)
    start_node = g.get_node(curr_add)  # O(n)
    dijkstras.run_dijkstras(g, start_node)  # O(n^2)

    for pkg_id in pkg_id_list:  # O(n^2)
        pkg = package_hash.lookup(pkg_id)  # O(n)

        # Skip the package if cannot be loaded on this truck
        if pkg.req_truck and pkg.req_truck != truck_id:
            continue

        end_node = g.get_node(pkg.address)  # O(n)

        if end_node.distance < min_pkg_distance:
            min_pkg_id = pkg_id
            min_pkg_distance = end_node.distance

    return min_pkg_id, min_pkg_distance


def sort_truck_dijkstras(truck, g, package_hash):
    """
    Sorts the packages on a truck, starting from the closest to the hub.

    *This version uses Dijkstra's Algorithm.*

    :param Truck truck: the truck being sorted
    :param Graph g: the Graph structure that Dijkstra's Algorithm has been run on
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return:
    """
    # Time complexity O(n^3)
    sorted_pkgs = list()
    sorted_distances = list()

    while len(sorted_pkgs) < len(truck.packages):  # O(n^3)
        if len(sorted_pkgs) == 0:
            curr_add = HUB_ADDRESS
        else:
            last_pkg = package_hash.lookup(sorted_pkgs[-1])  # O(n)
            curr_add = last_pkg.address

        pkg_list = list()
        for (pkg_id, _) in truck.packages:  # O(n)
            if pkg_id not in sorted_pkgs:
                pkg_list.append(pkg_id)

        min_pkg_id, min_pkg_distance = find_closest_pkg_dijkstras(curr_add, truck.id, pkg_list, g, package_hash)  # O(n^2)
        sorted_pkgs.append(min_pkg_id)
        sorted_distances.append(min_pkg_distance)

    truck.packages = list(zip(sorted_pkgs, sorted_distances))


def initiate_loading_dijkstras(truck_list, package_lists, g, package_hash):
    """
    Loads the truck with the packages from the package list.

    If more than one truck is given, trucks are loaded evenly by iterating over the trucks and loading the next package
    closest to its previously loaded package. After a package is loaded, the truck is sorted. This helps if there were
    sibling sets or other package lists loaded onto this truck previously.

    *This version uses Dijkstra's Algorithm.*

    :param list[Truck] truck_list: the trucks to be loaded
    :param list[str] package_lists: the package ids to be loaded
    :param Graph g: the Graph structure that Dijkstra's Algorithm has been run on
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return:
    """
    # Time complexity O(n^6)
    escape_condition = [True] * len(truck_list)

    for package_list in package_lists:  # O(n^6)
        eligible_pkg = True

        while len(package_list) > 0 and not [t.full() for t in truck_list] == escape_condition and eligible_pkg:  # O(n^5)
            for truck in truck_list:  # O(n^4)
                if not truck.full():
                    eligible_pkg = load_package_dijkstras(truck, package_list, g, package_hash)  # O(n^2)
                    sort_truck_dijkstras(truck, g, package_hash)  # O(n^3)


def load_siblings_dijkstras(truck_list, sibling_sets, package_lists, package_hash):
    """
    Loads packages onto the trucks that must be loaded together (sibling packages). Trucks are cycled after loading each
    sibling set. As siblings are loaded onto the trucks, they are removed from their associated package list.

    *This version uses Dijkstra's Algorithm.*

    :param list[Truck] truck_list: the trucks to be loaded
    :param list[set[str]] sibling_sets: the sets of package ids that must be loaded together
    :param list[list[str]] package_lists: the list of package id lists
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return:
    """
    # Time complexity O(n^3)
    i = 0
    curr_truck = truck_list[0]

    for sib_set in sibling_sets:  # O(n^3)
        for pkg in sib_set:  # O(n^2)
            curr_truck.add_package_dijkstras(pkg, float('inf'))
            package_hash.lookup(pkg).advance_status(curr_truck.time, curr_truck.id)  # O(n)

            # Remove package from any priority lists
            for package_list in package_lists:  # O(n)
                try:
                    package_list.remove(pkg)
                except ValueError:
                    pass

        # swap the truck to load next sibling_set
        i = 0 if i == len(truck_list) - 1 else i + 1

        curr_truck = truck_list[i]


def get_last_delayed_package(delayed, package_hash):
    """
    Gets the delayed package object with the latest delay time.

    :param list[str] delayed: the delayed package ids
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return: the latest delayed package
    :rtype: Package
    """
    # Time complexity O(n^2)
    last_delayed_pkg = None

    for pkg_id in delayed:  # O(n^2)
        pkg = package_hash.lookup(pkg_id)  # O(n)

        if not last_delayed_pkg:
            last_delayed_pkg = pkg
        else:
            if last_delayed_pkg.delay_time < pkg.delay_time:
                last_delayed_pkg = pkg

    return last_delayed_pkg


def get_return_order_of_trucks(truck_list):
    """
    Gets the list of trucks ordered by the time they return to the hub.

    :param list[Truck] truck_list: the trucks
    :return: the trucks ordered by time
    :rtype: list[Truck]
    """
    # Time complexity O(n^2)

    ordered_trucks = list()

    while len(truck_list) > 0:  # O(n^2)
        i = 0

        for truck in truck_list:  # O(n)
            if truck.time < truck_list[i].time:
                i = truck_list.index(truck)

        ordered_trucks.append(truck_list.pop(i))

    return ordered_trucks


# ********** THE FOLLOWING METHODS WERE USED IN A PREVIOUS VERSION AND ARE NOT CURRENTLY USED ***********

def load_package(truck, pkg_id_list, package_hash, location_hash):
    """
    .. warning:: THIS METHOD WAS USED IN A PREVIOUS VERSION AND IS NOT CURRENTLY USED. Use **load_package_dijkstras**
       instead.

    Loads the next package onto a truck.

    Nearest neighbor of the previous package added onto the truck is used to find the next package. If the truck is
    empty, then the nearest neighbor of the Hub is used.

    :param Truck truck: the truck being loaded
    :param list[str] pkg_id_list: the list of package ids currently being loaded from
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :param ChainingHashTable[str, Location] location_hash: the Location objects
    :return: True if a package was found to load onto the truck, False if no package was available to be loaded
    """
    if not truck.full() and len(pkg_id_list) > 0:
        if truck.last_package_dijkstras() == -1:
            truck_add = HUB_ADDRESS
        else:
            truck_add = package_hash.lookup(truck.last_package_dijkstras()).address

        next_pkg_id = find_closest_pkg(truck_add, truck, pkg_id_list, package_hash, location_hash)

        next_pkg = package_hash.lookup(next_pkg_id)

        if not next_pkg:
            return False
        else:
            truck.add_package(next_pkg_id)
            package_hash.lookup(next_pkg_id).advance_status(truck.time, truck.id)
            pkg_id_list.remove(next_pkg_id)
            return True


def find_closest_pkg(curr_add, truck_id, pkg_id_list, package_hash, location_hash):
    """
    .. warning:: THIS METHOD WAS USED IN A PREVIOUS VERSION AND IS NOT CURRENTLY USED. Use
       **find_closest_pkg_dijkstras** instead.

    Finds the nearest package destination to the current address that is allowed on the specific truck.

    :param str curr_add: the current address
    :param int truck_id: the id of the current truck
    :param list[str] pkg_id_list: the package ids currently being loaded
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :param ChainingHashTable[str, Location] location_hash: the Location objects
    :return: the id of the closest package destination, '-1' if none found
    :rtype: str
    """
    min_pkg_id = '-1'
    min_pkg_distance = float('inf')

    for pkg_id in pkg_id_list:
        pkg = package_hash.lookup(pkg_id)

        if pkg.req_truck and pkg.req_truck != truck_id:
            continue

        pkg_distance = location_hash.lookup(pkg.address).get_distance(curr_add)

        if pkg_distance < min_pkg_distance:
            min_pkg_id = pkg.id
            min_pkg_distance = pkg_distance

    return min_pkg_id


def sort_truck(truck, package_hash, location_hash):
    """
    .. warning:: THIS METHOD WAS USED IN A PREVIOUS VERSION AND IS NOT CURRENTLY USED. Use **sort_truck_dijkstras**
       instead.

    Sorts the packages on a truck, starting from the closest to the hub.

    :param Truck truck: the truck being sorted
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :param ChainingHashTable[str, Location] location_hash: the Location objects
    :return:
    """
    sorted_pkgs = list()

    while len(sorted_pkgs) < len(truck.packages):
        if len(sorted_pkgs) == 0:
            curr_add = HUB_ADDRESS
        else:
            last_pkg = package_hash.lookup(sorted_pkgs[-1])
            curr_add = last_pkg.address

        pkg_list = list()
        for pkg_id in truck.packages:
            if pkg_id not in sorted_pkgs:
                pkg_list.append(pkg_id)

        min_pkg_id = find_closest_pkg(curr_add, truck, pkg_list, package_hash, location_hash)
        sorted_pkgs.append(min_pkg_id)

    truck.packages = sorted_pkgs


def initiate_loading(truck_list, package_lists, package_hash, location_hash):
    """
    .. warning:: THIS METHOD WAS USED IN A PREVIOUS VERSION AND IS NOT CURRENTLY USED. Use
       **initiate_loading_dijkstras** instead.

    Loads the truck with the packages from the package list.

    If more than one truck is given, trucks are loaded evenly by iterating over the trucks and loading the next package
    closest to its previously loaded package. After a package is loaded, the truck is sorted. This helps if there were
    sibling sets or other package lists loaded onto this truck previously.

    :param list[Truck] truck_list: the trucks to be loaded
    :param list[str] package_lists: the package ids to be loaded
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :param ChainingHashTable[str, Location] location_hash: the Location objects
    :return:
    """

    escape_condition = [True] * len(truck_list)

    for package_list in package_lists:
        eligible_pkg = True

        while len(package_list) > 0 and not [t.full() for t in truck_list] == escape_condition and eligible_pkg:
            for truck in truck_list:
                if not truck.full():
                    eligible_pkg = load_package(truck, package_list, package_hash, location_hash)
                    sort_truck(truck, package_hash, location_hash)


def load_siblings(truck_list, sibling_sets, package_lists, package_hash):
    """
    .. warning:: THIS METHOD WAS USED IN A PREVIOUS VERSION AND IS NOT CURRENTLY USED. Use **load_siblings_dijkstras**
       instead.

    Loads packages onto the trucks that must be loaded together (sibling packages). Trucks are cycled after loading each
    sibling set. As siblings are loaded onto the trucks, they are removed from their associated package list.

    :param list[Truck] truck_list: the trucks to be loaded
    :param list[set[str]] sibling_sets: the sets of package ids that must be loaded together
    :param list[list[str]] package_lists: the list of package id lists
    :param ChainingHashTable[str, Package] package_hash: the Package objects
    :return:
    """
    i = 0
    curr_truck = truck_list[0]

    for sib_set in sibling_sets:
        for pkg in sib_set:
            curr_truck.add_package(pkg)
            package_hash.lookup(pkg).advance_status(curr_truck.time, curr_truck.id)

            # Remove package from any priority lists
            for package_list in package_lists:
                try:
                    package_list.remove(pkg)
                except ValueError:
                    pass

        # swap the truck to load next sibling_set
        i = 0 if i == len(truck_list) - 1 else i + 1

        curr_truck = truck_list[i]
