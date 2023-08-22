# Name: Joshua White
# OSU Email: whitejo4@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/09/2023
# Description: Implements a hashmap by utilizing chaining.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)                     # Represents the hash value found with the key
        index = hash % self._capacity                       # Represents the index the key and value will be added to
        chain = self._buckets[index]                        # Represents the linked list (chain) at the index

        if chain.remove(key) is True:                       # Checks for a duplicate key in the table, and replaces it
            chain.insert(key, value)
            return
        chain.insert(key, value)
        self._size += 1
        return

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return: An int value representing the number of empty buckets.
        """
        num = 0  # Represents the number of empty buckets found

        for element in range(self._capacity):
            chain = self._buckets[element]
            # Checks for empty linked lists (empty buckets)
            if chain.length() == 0:
                num += 1
        return num

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table.

        :return: A float value representing the load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map, without changing the underlying capacity.

        :return: None.
        """
        for element in range(self._capacity):
            self._buckets[element] = LinkedList()
        self._size = 0
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.

        :param new_capacity: Int value representing the new capacity.

        :return: None.
        """
        # Checks for a negative capacity value
        if new_capacity < 1:
            return
        # Checks for a prime number, and updates to the next prime number if not found
        elif self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        length = self._size                   # Represents the current size of the hash map.
        new_array = DynamicArray()            # Represents a temp dynamic array to house old values in hashmap
        empty_array = DynamicArray()          # Represents new empty array with updated capacity for hash map

        for element in range(self._capacity):
            new_array.append(self._buckets[element])
        for bucket in range(new_capacity):
            empty_array.append(LinkedList())

        self._capacity = new_capacity
        self._buckets = empty_array
        self._size = 0
        count = 0                             # Keeps track of the number of elements added to the hash map.
        indices = 0                           # Keeps track of the current index during iteration

        while count < length:
            chain = new_array[indices]
            if chain.length() != 0:
                for node in chain:
                    self.put(node.key, node.value)
                    count += 1
                indices += 1
            else:
                indices += 1
        return

    def get(self, key: str):
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
        chain = self._buckets[index]     # Represents the linked list (chain) at the index

        if chain.length() == 0:
            return None
        for node in chain:
            if node.key == key:
                return node.value

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
        chain = self._buckets[index]     # Represents the linked list (chain) at the index

        if chain.length() == 0:
            return False
        for node in chain:
            if node.key == key:
                return True
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
        chain = self._buckets[index]     # Represents the linked list (chain) at the index

        if chain.remove(key) is True:
            self._size -= 1
            return
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing tuples of all key/value pairs in a hash map.

        :return: Dynamic array with tuple values.
        """
        count = 0                   # Keeps track of the number of elements added to the hash map.
        indices = 0                 # Keeps track of the current index during iteration

        new_array = DynamicArray()  # Dynamic array that will contain tuple values from the hash map.

        while count < self._size:
            chain = self._buckets[indices]
            if chain.length() != 0:
                for node in chain:
                    new_array.append((node.key, node.value))
                    count += 1
                indices += 1
            else:
                indices += 1
        return new_array

    def find_mode_put(self, key: str, value=1) -> tuple:
        """
        Updates the key in a hash map, and uses the key's value to count the amount of duplicates of that same key.

        :param key: The key that will be added to the hash map.
        :param value: Represents the number of times a key has been added to the hashmap.

        :return: Returns the key and value that was added.
        """
        # Checks to see if the table needs to be resized.
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)                # Represents the hash value found with the key
        index = hash % self._capacity                  # Represents the index the key and value will be added to
        chain = self._buckets[index]                   # Represents the linked list (chain) at the index

        duplicates = self.get(key)

        if chain.remove(key) is True:                  # Checks for a duplicate key in the table, and updates the value
            chain.insert(key, value + duplicates)
            return key, value + duplicates
        chain.insert(key, value)
        self._size += 1
        return key, value


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode of a dynamic array, using a hash map.

    :param da: Dynamic array that the mode will derive from.

    :return: A dynamic array an int value representing the frequency of the mode.
    """
    map = HashMap()                             # Hash map that will contain key/values derived from da array
    mode_array = DynamicArray()                 # Array that will contain modes found in hash map
    frequency = None                            # Represents the current frequency for mode

    for num in range(da.length()):
        pair = map.find_mode_put(da[num])       # Adds values into hash map and returns the key/value pair added
        value = pair[1]
        if mode_array.length() == 0:
            mode_array.append(pair[0])
            frequency = value
        elif frequency == value:
            mode_array.append(pair[0])
        # if new key/value pair has a higher frequency, replaces mode_array with new array containing new pair
        elif frequency < value:
            mode_array = DynamicArray()
            mode_array.append(pair[0])
            frequency = value
    return mode_array, frequency


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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
