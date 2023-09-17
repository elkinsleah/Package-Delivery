# Creates class for the Hash Table
class HashTable:

    # Constructor. O(n)
    def __init__(self, initial_capacity=20):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    # Inserts a new item into the hash table and updates the item. O(n)
    def insert(self, key, item):
        # Gets the bucket list where the item will go.
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # Update the key if it is already in the bucket.
        for key_val in bucket_list:
            # Print key_value
            if key_val[0] == key:
                key_val[1] = item
                return True

        # If not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches items in the hash table. O(n)
    def search(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        # Returns None if the item is not found.
        for key_val in bucket_list:
            if key == key_val[0]:
                return key_val[1]
        return None

    # Removes item from the hash table. O(n)
    def remove(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        # The item is removed if the key is found in the hash table.
        if key in bucket_list:
            bucket_list.remove(key)