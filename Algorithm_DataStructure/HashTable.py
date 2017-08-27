# Write a HashTable class that stores strings
# in a hash table, where keys are calculated using
# the first two letters of the string.

class HashTable(object):
    def __init__(self):
        self.table = [None] * 10000

    def calculate_hash_value(self,string):
        if len(string)>=2:
            hash_value = ord(string[0]) * 100 + ord(string[1])
            return hash_value
        else:
            return -1

    def lookup(self,string):
        '''Return the hash value if the string is already in the table
        Otherwise,return -1'''
        string_hash_value = self.calculate_hash_value(string)
        if string_hash_value != -1:
            if self.table[string_hash_value] != None:
                if string in self.table:
                    return string_hash_value
        return -1
       # if self.table[string_hash_value] == string:
        #    return string_hash_value
        #else:
        #    return -1

    def store(self,string):
        string_hash_value = self.calculate_hash_value(string)
        if string_hash_value != -1:
            if self.table[string_hash_value] != None:
                self.table[string_hash_value].append(string)
            else:
                self.table[string_hash_value] = string



hash_table = HashTable()
print hash_table.calculate_hash_value('UDACITY')
print hash_table.lookup('UDACITY')

hash_table.store('UDACITY')

print hash_table.lookup('UDACITY')

#Test store edge case
hash_table.store('UDACIOUS')
print hash_table.lookup('UDACIOUS')
