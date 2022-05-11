class ChainingHashTable:
    """
    Hash table that uses a finite number of buckets, each containing a list of values that all hash to that bucket
    location.

    The list for each bucket helps deal with collisions, but increases the time complexity for accessing a value.
    Entries to this hash table are in key-value pairs. The key is hashed and the key-value pair is stored as a list of
    length 2.
    """
    def __init__(self, num_buckets):
        """
        Creates a list (the hash table) with a length of the specified buckets.

        Each entry in the list contains another empty list to hold the values that hash to that bucket.

        :param int num_buckets: the number of buckets to use for the hash table.
        """
        # Time complexity O(n)
        self.table = list()

        for i in range(num_buckets):
            self.table.append(list())

    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash table.

        The key is hashed and must uniquely identify the value.

        :param key: the unique key to be hashed and to identify the value, must be a hashable type
        :param value: the value stored
        """
        # Time complexity O(1)
        bucket = self.hash(key)
        self.table[bucket].append([key, value])

    def lookup(self, key):
        """
        Lookup a value in the hash table by its unique key.

        The key is hashed to identify the bucket. The elements of that bucket are to find one that matches the specified
        key. If the key is found, the associated value is returned. If not, None is returned.

        :param key: the unique key of the value being searched for
        :return: the associated value if the key is found, None if the the key is not found
        """
        # Time complexity O(n)
        bucket = self.hash(key)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]

        return None

    def remove(self, key):
        """
        Removes a key-value pair from the hash table.

        The lookup method is used to find the value. If the value is found, the key is hashed to get the bucket and
        the key-value pair is removed.

        :param key: the unique key of the value to be removed
        :return: True if the key is found and key-value pair removed, False if the key is not found
        """
        # Time complexity O(n)
        value = self.lookup(key)  # O(n)

        if value:
            bucket = self.hash(key)
            self.table[bucket].remove([key, value])
            return True
        else:
            return False

    def hash(self, key):
        """
        Hashes the key and limits the possible values to the number of buckets.

        :param key: the key to be hashed
        :return: the hashed key
        """
        # Time complexity O(1)
        return hash(key) % len(self.table)

    def __str__(self):
        """
        Provide a string representation of the ChainingHashTable.

        :return: string value of the ChainingHashTable
        """
        # Time complexity O(n)
        s = ''

        for i in range(len(self.table)):
            s += str(i) + ': ' + str(self.table[i]) + '\n'

        return s.strip('\n')

    def __len__(self):
        """
        Provide the number of entries in the hash table.

        :return: number of entries in the hash table
        :rtype: int
        """
        # Time complexity O(n)
        sum_len = 0

        for bucket in self.table:
            sum_len += len(bucket)

        return sum_len


