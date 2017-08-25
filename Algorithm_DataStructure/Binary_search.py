# A binary search function
# input : a list to search ; the value you're searching for
# output : the index of value or -1 if the value doesn't in this
#          list
# Note: the input list contains distinct value and has an
#       increasing order.

def binary_search(input_array,value):
    com_array = input_array
    current_index = None
    fact_index = None
    former_index = 0
    while len(com_array) > 0:

        n = len(com_array)

        if n == 1 or n == 2:
            current_index = 0

        elif n > 0 and (n % 2 == 0):
            current_index = n / 2 - 1

        else:
            current_index = int( n / 2 )

        com_value = com_array[current_index]


        fact_index = current_index + former_index


        if value < com_value:
            com_array = com_array[0:current_index]


        if value > com_value:
            com_array = com_array[current_index+1:]

            former_index = fact_index + 1


        if value == com_value:
            return fact_index

    return -1


test_list = [1,3,9,11,15,19]
test_val1 = 1
test_val2 = 11
#print binary_search(test_list, test_val1)
#print binary_search(test_list, test_val2)

#--This way to do binarySearch is so deft!!!!!!!!

def binarySearch(ListData,value):
    low = 0
    high = len(ListData) - 1
    while (low <= high):
        mid = (low + high ) / 2
        if (ListData[mid] == value):
            return mid
        elif(ListData[mid] < value):
            low = mid + 1
        else:
            high = mid - 1
    return -1

print binarySearch(test_list, test_val1)
print binarySearch(test_list, test_val2)
