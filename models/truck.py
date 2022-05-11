class Truck:
    """
    Represents a delivery truck and keeps track of the packages loaded on to it.
    """
    SPEED = 18.0 # mph
    MAX_PKGS = 16

    def __init__(self, tid, time, start_address):
        # Time complexity O(1)
        self.id = tid
        self.time = time
        self.distance = 0
        self.packages = list()
        self.current_address = start_address

    def add_package_dijkstras(self, pkg_id, pkg_dist):
        """
        If there is room on the truck, the package is added to the truck.

        *This version uses Dijkstra's Algorithm.*

        :param float pkg_dist: distance of the shortest path to the package
        :param string pkg_id: the id of the package to add to the truck
        :return: True if successful
        """
        # Time complexity O(1)

        if len(self.packages) < Truck.MAX_PKGS:
            self.packages.append((pkg_id, pkg_dist))
            return True
        else:
            print(f'Truck {self.id} is at max capacity of {Truck.MAX_PKGS}.')
            return False

    def deliver(self):
        """
        Pops the first package off the package list and returns the package ID.

        :return: id of first package on package list
        :rtype: str
        """
        # Time complexity O(1)
        return self.packages.pop(0)

    def peek(self):
        """
        Checks what the next package id is, but does not remove it from the truck.

        :return: the id of the next package to be delivered, None if the truck is empty
        :rtype: str
        """
        # Time complexity O(1)

        if len(self.packages) > 0:
            return self.packages[0]
        else:
            None

    def full(self):
        """
        Checks to see if the truck is full.

        :return: True if the truck is full
        """
        # Time complexity O(1)

        return len(self.packages) >= Truck.MAX_PKGS

    def empty(self):
        """
        Checks if the truck is empty.

        :return: True if the truck is empty
        """
        # Time complexity O(1)

        return len(self.packages) == 0

    def last_package_dijkstras(self):
        """
        Gets the id of the last package to be delivered.

        *This version uses Dijkstra's Algorithm.*

        :return: id of the last package
        :rtype: str
        """
        # Time complexity O(1)

        if len(self.packages) == 0:
            return -1
        else:
            return self.packages[-1][0]

    # ************* THE FOLLOWING METHODS WERE USED IN A PREVIOUS VERSION. THEY ARE NOT CURRENTLY USED **************

    def add_package(self, pkg_id):
        """
        If there is room on the truck, the package is added to the truck.

        .. warning:: USED IN A PREVIOUS VERSION. NOT CURRENTLY USED.
           Use **add_package_dijkstras** instead.

        :param pkg_id: the id of the package to add to the truck
        :return: True if successful
        """
        # Time complexity O(1)

        if len(self.packages) < Truck.MAX_PKGS:
            self.packages.append(pkg_id)
            return True
        else:
            print(f'Truck {self.id} is at max capacity of {Truck.MAX_PKGS}.')
            return False

    def last_package(self):
        """
        Gets the id of the last package to be delivered.

        .. warning:: USED IN A PREVIOUS VERSION. NOT CURRENTLY USED.
           Use **last_package_dijkstras** instead.

        :return: id of the last package
        :rtype: str
        """
        # Time complexity O(1)

        if len(self.packages) == 0:
            return -1
        else:
            return self.packages[-1]