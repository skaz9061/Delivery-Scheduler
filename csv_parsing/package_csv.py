import csv
from datetime import datetime, time

from data_structures.chaining_hash_table import ChainingHashTable
from models.package import Package
from utils import TIME_FORMAT


def read():
    """
    Parses the csv file for the packages and creates the associated package lists and package objects.

    :return: a tuple containing the following data in order:

        - ChainingHashTable of the package objects representing each package
        - List of package ids with priority 1
        - List of package ids with priority 2
        - List of package ids with priority 3
        - List of package ids with 'Delayed' status
        - List of sets that contain the package ids that must be delivered on the same truck (sibling sets)
    """
    # Time complexity O(n^3)
    with open("assets/WGUPS Package File.csv", encoding="utf-8-sig") as csvfile:
        package_raw = csv.reader(csvfile, dialect='excel')

        # Get first row and parse headers
        headers = next(package_raw)
        headers = [str(x).upper() for x in headers]

        package_hash = ChainingHashTable(10)
        delayed = []
        priority_1 = []
        priority_2 = []
        priority_3 = []
        all_sibling_sets = list()

        for row in package_raw:  # O(n^3)
            pid = None
            address = None
            deadline = Package.PRIORITY_3
            city = None
            state = None
            zipcode = None
            weight = None
            req_truck = None
            status = Package.AT_HUB
            siblings = set()
            delay_time = None

            for i in range(len(row)):  # O(n^2)
                header = headers[i]

                if header == 'ID':
                    pid = row[i]
                elif header == 'ADDRESS':
                    address = row[i]
                elif header == 'DEADLINE':
                    if row[i] != "EOD":
                        deadline = datetime.strptime(row[i], TIME_FORMAT).time()
                elif header == 'CITY':
                    city = row[i]
                elif header == 'STATE':
                    state = row[i]
                elif header == 'ZIP':
                    zipcode = row[i]
                elif header == 'WEIGHT':
                    weight = row[i]
                elif header == 'SPECIAL NOTES':
                    if row[i] != '':
                        note_parts = row[i].upper().split(' ')

                        if 'TRUCK' in note_parts:
                            req_truck = int(note_parts[-1])
                        elif note_parts[0:4] == ['MUST', 'BE', 'DELIVERED', 'WITH']:
                            siblings = note_parts[4:]
                            siblings = [s.strip(',') for s in siblings]
                            new_sibling_set = set(siblings)
                            new_sibling_set.add(pid)

                            found = False
                            for sibling_set in all_sibling_sets:  # O(n)
                                if len(new_sibling_set.intersection(sibling_set)) != 0:
                                    found = True
                                    sibling_set.update(new_sibling_set)
                                    break

                            if not found:
                                all_sibling_sets.append(new_sibling_set)

                        elif 'DELAYED' in note_parts:
                            status = Package.DELAYED
                            delay_time = datetime.strptime(f'{note_parts[-2]} {note_parts[-1]}', TIME_FORMAT).time()
                        elif note_parts[0:2] == ['WRONG', 'ADDRESS']:
                            status = Package.DELAYED
                            delay_time = time(10, 20)
                        else:
                            print(f'Error parsing Special Note: {row[i]}')
                else:
                    print(f'Error parsing column: {header}')

            new_package = Package(pid, address, deadline, city, state, zipcode,
                                  weight, status, delay_time, req_truck, siblings)

            package_hash.insert(new_package.id, new_package)

            if new_package.status == Package.DELAYED:
                delayed.append(new_package.id)
            elif new_package.deadline == Package.PRIORITY_1:
                priority_1.append(new_package.id)
            elif new_package.deadline == Package.PRIORITY_2:
                priority_2.append(new_package.id)
            else:
                priority_3.append(new_package.id)

        return package_hash, priority_1, priority_2, priority_3, delayed, all_sibling_sets
