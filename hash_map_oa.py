# Name: Joshua White
# OSU Email: whitejo4@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/09/23
# Description: Implements a hash map utilizing open addressing with quadratic probing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key and value pair of a hash map.

        :param key: The key that will be added to the hash map.
        :param value: The value that will be added to the hash map.

        :return: None.
        """
        # Checks to see if the table needs to be resized.
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)  # Represents the hash value found with the key
        index = hash % self._capacity    # Represents the index the key and value will be added to
        count = 1                        # Variable for quadratic probing formula

        if self._buckets[index] is not None:                        # Checks for occupied buckets
            if self._buckets[index].is_tombstone is True:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return
            elif self._buckets[index].key == key:                   # Checks for duplicates
                self._buckets[index].value = value
                return
            # Iterates through with quadratic probing until an empty space is found for hash entry
            for bucket in range(self._capacity):
                quad_probe = (index + (count ** 2)) % self._capacity
                if self._buckets[quad_probe] is None or self._buckets[quad_probe].is_tombstone is True:
                    self._buckets[quad_probe] = HashEntry(key, value)
                    self._size += 1
                    return
                elif self._buckets[quad_probe].key == key:
                    self._buckets[quad_probe].value = value
                    return
                count += 1
        else:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
            return

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table.

        :return: A float value representing the load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return: An int value representing the number of empty buckets.
        """
        num = 0  # Represents the number of empty buckets found

        for element in range(self._capacity):
            if self._buckets[element] is None or self._buckets[element].is_tombstone is True:
                num += 1
        return num

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.

        :param new_capacity: Int value representing the new capacity.

        :return: None.
        """
        # Checks for a negative capacity value
        if new_capacity < self._size:
            return
        # Checks for a prime number, and updates to the next prime number if not found
        elif self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        length = self._size             # Represents the current size of the hash map.
        new_array = DynamicArray()      # Represents a temp dynamic array to house old values in hashmap
        empty_array = DynamicArray()    # Represents new empty array with updated capacity for hash map

        for element in range(self._capacity):
            if self._buckets[element] is not None and self._buckets[element].is_tombstone is False:
                new_array.append(self._buckets[element])
        for bucket in range(new_capacity):
            empty_array.append(None)

        self._capacity = new_capacity
        self._buckets = empty_array
        self._size = 0
        count = 0      # Keeps track of the number of elements added to the hash map.
        indices = 0    # Keeps track of the current index during iteration

        while count < length:
            bucket = new_array[indices]
            self.put(bucket.key, bucket.value)
            count += 1
            indices += 1
        return

    def get(self, key: str) -> object:
        """
        Returns a node value, using the associated key in the hash map.

        :param key: Represents the key, the value will be derived from.

        :return: The key's value.
        """
        # Checks for an empty hash map
        if self._size == 0:
            return None

        hash = self._hash_function(key)  # Represents the hash value found with the key
        index = hash % self._capacity    # Represents the index the key and value will be added to
        count = 1                        # Variable for quadratic probing formula

        if self._buckets[index] is None:
            return None
        elif self._buckets[index].key == key:
            return self._buckets[index].value
        # Iterates through with quadratic probing until key or None is found
        for bucket in range(self._capacity):
            quad_probe = (index + (count ** 2)) % self._capacity
            if self._buckets[quad_probe] is None:
                return None
            elif self._buckets[quad_probe].key == key:
                return self._buckets[quad_probe].value
            count += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Searches for a given key in the hash map.

        :param key: The key that the method will search for.

        :return: A boolean value representing whether or not the key was found.
        """
        # Checks for an empty hash map
        if self._size == 0:
            return False

        hash = self._hash_function(key)  # Represents the hash value found with the key
        index = hash % self._capacity    # Represents the index the key and value will be added to
        count = 1                        # Variable for quadratic probing formula

        if self._buckets[index] is None:
            return False
        elif self._buckets[index].key == key:
            return True
        # Iterates through with quadratic probing until key or None is found
        for bucket in range(self._capacity):
            quad_probe = (index + (count ** 2)) % self._capacity
            if self._buckets[quad_probe] is None:
                return False
            elif self._buckets[quad_probe].key == key:
                return True
            count += 1
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key from the hash map.

        :param key: The key that will be removed.

        :return: None.
        """
        # Checks for an empty hash map
        if self._size == 0:
            return

        hash = self._hash_function(key)  # Represents the hash value found with the key
        index = hash % self._capacity    # Represents the index the key and value will be added to
        count = 1                        # Variable for quadratic probing formula

        if self._buckets[index] is None:
            return
        elif self._buckets[index].key == key:
            if self._buckets[index].is_tombstone is True:
                return
            self._buckets[index].is_tombstone = True
            self._size -= 1
            return
        # Iterates through with quadratic probing until key or None is found
        for bucket in range(self._capacity):
            quad_probe = (index + (count ** 2)) % self._capacity
            if self._buckets[quad_probe] is None:
                return
            elif self._buckets[quad_probe].key == key:
                if self._buckets[quad_probe].is_tombstone is True:
                    return
                self._buckets[quad_probe].is_tombstone = True
                self._size -= 1
                return
            count += 1
        return

    def clear(self) -> None:
        """
        Clears the contents of the hash map, without changing the underlying capacity.

        :return: None.
        """
        for element in range(self._capacity):
            self._buckets[element] = None
        self._size = 0
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing tuples of all key/value pairs in a hash map.

        :return: Dynamic array with tuple values.
        """
        new_array = DynamicArray()  # Array that will be returned with tuple values

        for element in range(self._capacity):
            if self._buckets[element] is not None and self._buckets[element].is_tombstone is False:
                new_array.append((self._buckets[element].key, self._buckets[element].value))
        return new_array

    def __iter__(self):
        """
        Create iterator for loop.
        """
        temp = 0
        if self._buckets[temp] is None or self._buckets[temp].is_tombstone is True:
            for element in range(self._capacity):
                temp += 1
        self._index = temp
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        try:
            value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration
        self._index = self._index + 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
