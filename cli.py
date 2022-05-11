# Module for the command line interface
# Time complexities for this module are largely user-driven
import itertools
from datetime import date
import utils


def control(truck_list, package_lists, package_hash):
    """
    Main control for the CLI.

    Serves the main menu and controls the actions taken by each menu choice. After each menu choice, the program
    is looped back to the main menu. Once the control method is invoked, the program does not leave this method
    until the user chooses to exit.

    :param list[Truck] truck_list: list of truck objects
    :param list[list[str]] package_lists: list of lists of package ids (i.e. delayed and priority lists)
    :param ChainingHashTable[str, Package] package_hash: ChainingHashTable of package objects
    :return:
    """
    user_exit = False
    max_choice = 6
    min_choice = 1
    choice = 0

    print()
    print(f'WGUPS Package Delivery Tracking - {date.today()}')
    print()

    while not user_exit:
        while choice < min_choice or choice > max_choice:
            print('Main menu')
            print('1. Final Truck Statistics')
            print('2. Final Package Info (single)')
            print('3. Final Package Info (all)')
            print('4. Package Time Snapshot (single)')
            print('5. Package Time Snapshot (all)')
            print('6. Exit')
            print()

            try:
                choice = int(input('Enter the number of your selection: '))
                if choice < min_choice or choice > max_choice:
                    print(f'ERROR Must enter a number between {min_choice} and {max_choice}')
            except ValueError:
                print('ERROR Must enter an integer.')
                print()
                choice = 0

        print()
        if choice == 1:
            print_final_statistics(truck_list, package_lists)
        elif choice == 2:
            id = get_package_id(1, len(package_hash))
            print()
            print_package(id, package_hash)
        elif choice == 3:
            print_all_packages(package_hash)
        elif choice == 4:
            id = get_package_id(1, len(package_hash))
            time = get_user_time()
            print()
            print_snapshot(id, time, package_hash)
        elif choice == 5:
            time = get_user_time()
            print_all_snapshots(time, package_hash)
        elif choice == 6:
            print('Goodbye.')
            user_exit = True

        if choice != 6:
            print()
            input('Press Enter to return to Main Menu...')
            print()

            choice = 0


def print_final_statistics(truck_list, package_lists):
    """
    Prints the final stats of the trucks, distance traveled, and number of remaining packages.

    :param list[Truck] truck_list: the list of truck objects
    :param list[list[str]] package_lists: the list of lists of package ids
    :return:
    """
    for truck in truck_list:
        print(f'Truck {truck.id}: \n\tfinished @ {str(truck.time)}\n\ttraveled {truck.distance} miles')

    print(f'Total Distance: {sum([truck.distance for truck in truck_list])}')
    print(f'Packages left: {len(list(itertools.chain(*package_lists)))}')


def print_all_packages(package_hash):
    """
    Prints all packages in their final state, in ascending package id order.

    :param ChainingHashTable[str, Package] package_hash: Chaining hash table of Package objects
    :return:
    """
    for index in range(len(package_hash)):
        print_package(index + 1, package_hash)
        print()


def print_package(id, package_hash):
    """
    Prints a specific package in its final state

    :param str id: the id of the package
    :param ChainingHashTable[str, Package] package_hash: ChainingHashTable of Package objects
    :return:
    """
    print(package_hash.lookup(str(id)))


def print_all_snapshots(time, package_hash):
    """
    Prints all packages in the state they were in at a specific time.

    :param datetime.time time: the time for the snapshots
    :param ChainingHashTable[str, Package] package_hash: ChainingHashTable of Package objects
    :return:
    """
    for index in range(len(package_hash)):
        print_snapshot(index + 1, time, package_hash)
        print()


def print_snapshot(id, time, package_hash):
    """
    Prints a specific package in the state it was in at a specific time.

    :param datetime.time time: the time for the snapshot
    :param ChainingHashTable[str, Package] package_hash: ChainingHashTable of Package objects
    :return:
    """
    package_hash.lookup(str(id)).print_snapshot(time)


def get_user_time():
    """
    Prompt the user for a time in the correct format.

    If an invalid entry is given, the prompt is repeated until a valid entry is given.

    :return: the user-given time
    :rtype: datetime.time
    """
    final_time = None

    while not final_time:
        user_time = input('\nPlease enter a time in the format HH:MM AM/PM: ')

        try:
            final_time = utils.str_to_time(user_time, utils.TIME_FORMAT)
        except ValueError:
            print('ERROR incorrect time format.')
            final_time = None

    return final_time


def get_package_id(min, max):
    """
    Prompt the user for a package id. Package id must be an int.

    :param int min: the minimum acceptable value for the package id
    :param int max: the maximum acceptable value for the package id
    :return: the user-given package id
    :rtype: int
    """
    choice = min - 1

    while choice > max or choice < min:
        try:
            choice = int(input('\nEnter the package ID: '))

            if choice > max or choice < min:
                print(f'ERROR Package ID must be between {min} and {max}.')

        except ValueError:
            print('ERROR Package ID must be an Integer.')

    return choice
