import csv
from data_structures.chaining_hash_table import ChainingHashTable
from models.location import Location


def read():
    """
    Parses the csv file for possible locations and their distances from one another.

    :returns: a ChainingHashTable of the Location objects representing each location.
    """
    # Time complexity O(n^3)
    with open('assets/WGUPS Distance Table.csv') as csvfile:
        location_raw = csv.reader(csvfile, dialect='excel')

        headers = next(location_raw)
        address_refs = list()

        # remove unneeded headers
        headers[0] = ''
        headers[1] = ''

        for address in headers: # O(n)
            if address != '':
                address_parts = str(address).split('\n')
                address_parts[1] = address_parts[1].strip(' ,')
                address_refs.append(address_parts[1])
            else:
                address_refs.append(address)

        location_hash = ChainingHashTable(10)  # O(n)

        for row in location_raw:  # O(n^3)
            # Parsing data for Location object
            name_address_parts = row[0].split('\n')
            name = name_address_parts[0]
            address = name_address_parts[1].strip(' ')

            zip_i = row[1].index('(') + 1
            zipcode = row[1][zip_i:(zip_i + 5)]

            # Creating the Location Object
            new_loc = Location(address, zipcode, name)

            # Adding destinations and distances to Location
            for i in range(2, len(row)):  # O(n^2)
                if row[i] != '' and row[i] != '0.0':
                    new_loc.add_destination(address_refs[i], row[i])

                    # Adding distance for reverse direction
                    other_loc = location_hash.lookup(address_refs[i])  # O(n)
                    if other_loc is None:
                        print(f'Cannot add distance for {address_refs[i]}, location not found in hash table.')
                    else:
                        other_loc.add_destination(new_loc.address, row[i])

            # Add Location to its own destinations
            new_loc.add_destination(new_loc.address, '0.0')

            # Add the new Location object to the hash table
            location_hash.insert(new_loc.address, new_loc)

        return location_hash
