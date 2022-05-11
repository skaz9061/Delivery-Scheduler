from datetime import time
import utils


class Package:
    """
    Represents a package to be delivered.
    """
    # Values for package status
    DELAYED = "Delayed"
    AT_HUB = "At Hub"
    EN_ROUTE = "En Route"
    DELIVERED = "Delivered"

    # Values for package priority based on delivery time
    PRIORITY_1 = time(9)       # 9:00 AM
    PRIORITY_2 = time(10, 30)  # 10:30 AM
    PRIORITY_3 = time(23, 59)  # 11:59 PM or EOD

    def __init__(self, pid, address, deadline, city, state, zipcode, weight, status=AT_HUB, delay_time=None, req_truck=None, siblings=[]):
        # Time complexity O(1)

        self.id = pid
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.weight = weight
        self.status = status
        self.req_truck = req_truck
        self.siblings = siblings  # siblings are packages that it must be delivered with
        self.delay_time = delay_time
        self.at_hub_time = time(0)
        self.en_route_time = None
        self.delivered_time = None
        self.delivery_truck = None

    def __str__(self):
        """
        Provides string representation of the package object. String varies based on the status of the package.

        :return: the string value of the object
        """
        # Time complexity O(1)

        s = f'Package {self.id}: {self.address}, {self.city}, {self.state} {self.zipcode} \n ' \
            f'\tWeight: {self.weight} KG \t Due: {self.deadline.strftime("%I:%M %p")} \tReq. Truck: {self.req_truck} \n' \
            f'\tStatus: {self.status} '

        if self.status == Package.DELAYED:
            s += f' until {self.delay_time.strftime("%I:%M %p")}'
        else:
            s += f' as of '

            if self.status == Package.AT_HUB:
                s += self.at_hub_time.strftime("%I:%M %p")
            elif self.status == Package.EN_ROUTE:
                s += self.en_route_time.strftime("%I:%M %p")
                s += f' on Truck {self.delivery_truck}'
            else:
                s += self.delivered_time.strftime("%I:%M %p")
                s += f' by Truck {self.delivery_truck}'
                s += '\t\tOn-Time: '
                s += str(self.delivered_time <= self.deadline)

        return s

    def advance_status(self, curr_time, truck_id=None):
        """
        Advances status of package to the next logical status and tracks the time the status change was made.

        :param int truck_id: id of the truck the package is on or delivered by
        :param datetime.time curr_time: time of the status change
        :return:
        """
        # Time complexity O(1)

        if self.status == Package.AT_HUB:
            self.status = Package.EN_ROUTE
            self.en_route_time = curr_time
        elif self.status == Package.DELAYED:
            self.status = Package.AT_HUB
            self.at_hub_time = self.delay_time
        else:
            self.status = Package.DELIVERED
            self.delivered_time = curr_time

        if truck_id is not None:
            self.delivery_truck = truck_id

    def print_snapshot(self, time):
        """
        Prints a snapshot of the package in the state it would have been at the time specified.

        :param datetime.time time: the time for the snapshot of the package's state
        :return:
        """
        # Time complexity O(1)

        orig_status = self.status

        if self.delay_time and time < self.delay_time:
            self.status = Package.DELAYED
        elif time < self.en_route_time:
            self.status = Package.AT_HUB
        elif time < self.delivered_time:
            self.status = Package.EN_ROUTE

        print(f'*** Snapshot at {utils.time_str(time, utils.TIME_FORMAT)} ***')
        print(self)

        self.status = orig_status
