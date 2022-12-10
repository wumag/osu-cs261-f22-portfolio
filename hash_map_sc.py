# Name: Maggie Wu
# OSU Email: wumag@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap
# Due Date: 12/2/2022
# Description: Implement the HashMap class using a dynamic array to store a hash table, and implement chaining for
# collision resolution using a singly linked list.


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
        Update the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a new key/value pair must be added.
        :param key: string to be added
        :param value: object to be added
        :return: none
        """
        # table must be resized to double its current
        # capacity when this method is called and the current load factor of the table is
        # greater than or equal to 1.0
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)  # compute a value based on the key
        index = hash % self._capacity  # makes sure the value gets assigned to an index that exists in the array

        if self._buckets[index].contains(key):
            self._buckets[index].contains(key).value = value  # replace old value with new value if key exists
        else:  # if key does not exist
            self._buckets[index].insert(key, value)  # insert new key/value pair if key does not exist
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table.
        :return: number of empty buckets
        """
        count = 0
        for i in range(self._buckets.length()):
            if self._buckets[i].length() == 0:  # check if bucket is empty
                count += 1
        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        :return: hash table load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clear the contents of the hash map without changing the underlying hash table capacity.
        :return: none
        """
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal hash table. All existing key/value pairs
        must remain in the new hash map, and all hash table links must be rehashed.
        If new_capacity is not less than 1, the method does nothing.
        If new_capacity is 1 or more, make sure it is a prime number. If not, change it to the next
        highest prime number.
        :param new_capacity: capacity of internal hash table
        :return: none
        """
        if new_capacity < 1:  # do nothing if new_capacity is less than 1
            return

        if self._is_prime(new_capacity) is False:  # change non-prime number to next highest prime number
            new_capacity = self._next_prime(new_capacity)

        new_hash_map = DynamicArray()  # create new array with new_capacity
        for i in range(self._capacity):
            new_hash_map.append(self._buckets[i])  # append elements onto new hash map

        self.clear()
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        for i in range(new_capacity):
            self._buckets.append(LinkedList())

        for i in range(new_hash_map.length()):
            for j in new_hash_map[i]:
                self.put(j.key, j.value)  # rehash into new hash map

    def get(self, key: str):
        """
        Return the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        :param key: string/key associated with value
        :return: string/key associated with value or none
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].contains(key):  # check if key exists
            return self._buckets[index].contains(key).value  # return the associated value

    def contains_key(self, key: str) -> bool:
        """
        Return True if the given key is in the hash map, otherwise it returns False.
        :param key: string to search for in the hash map
        :return: True or False
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].contains(key):  # check if key exists
            return True
        else:  # key does not exist
            return False

    def remove(self, key: str) -> None:
        """
        Remove the given key and its associated value from the hash map.
        :param key: string to remove in the hash map
        :return: none
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].contains(key):  # check if key exists
            self._buckets[index].remove(key)  # removes first node with matching key
            self._size -= 1  # decrement size if removal successful

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        :return: dynamic array consisting of key/value pairs
        """
        new_array = DynamicArray()
        for i in range(self._buckets.length()):
            for j in self._buckets[i]:
                new_array.append((j.key, j.value))  # store tuples of key/value pairs in new array
        return new_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Return a tuple containing, in this order, a dynamic array comprising the mode (most occurring) value/s of the array,
    and an integer that represents the highest frequency (how many times they appear).
    :param da: dynamic array to be calculated
    :return: dynamic array with tuples containing mode and highest frequency
    """
    map = HashMap()
    max_frequency = 0
    mode_array = DynamicArray()

    for i in range(da.length()):
        key = da[i]
        if map.contains_key(key):  # if key exists
            frequency = map.get(key)  # return value associated with key
            map.put(key, frequency + 1)  # update array with element and increment count
            if frequency + 1 > max_frequency:  # set max
                max_frequency = frequency + 1
        else:  # if key does not exist, frequency is 1
            if max_frequency == 0:
                max_frequency = 1
            map.put(key, 1)
    for i in range(map.get_capacity()):
        for j in map._buckets[i]:
            if j.value == max_frequency:  # if bucket's value is the same as max
                mode_array.append(j.key)  # add bucket's key to the array
            elif j.value > max_frequency:
                max_frequency = j.value
                mode_array = DynamicArray()
                mode_array.append(j.value)
    return mode_array, max_frequency

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
