class Location:
    """
    Represents a physical location and the distances to all other possible destinations from this location.
    """
    def __init__(self, address, zipcode, name):
        # Time complexity O(1)

        self.address = address
        self.zipcode = zipcode
        self.name = name
        self.destinations = dict()

    def __str__(self):
        """
        Provides a string representation of this location.

        :return: the string value of this location
        """
        # Time complexity O(1)

        s = ''
        s += self.name + '\n'
        s += self.address + '\n'
        s += self.zipcode

        return s

    def add_destination(self, address, distance):
        """
        Add a possible destination from this location.

        :param string address: the address of the destination
        :param float distance: the distance to the destination
        :return:
        """
        # Time complexity O(1)

        self.destinations[address] = float(distance)

    def get_distance(self, address):
        """
        Gets the distance to a destination.

        :param string address: the address of the destination
        :return: the distance to the destination
        :rtype: float
        """
        # Time complexity O(1)

        return self.destinations[address]

