# Question 8: Longest Repetition

# Define a procedure, longest_repetition, that takes as input a
# list, and returns the element in the list that has the most
# consecutive repetitions. If there are multiple elements that
# have the same number of longest repetitions, the result should
# be the one that appears first. If the input list is empty,
# it should return None.

#Watch out !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#consecutive repetitions!!!!!!!!!!!!!!!!!!!


def longest_repetition(some):# input: list output: one element or None
    # count of element
    counted=[]
    max = 0
    longest = None
    for element in some:
     #  print element
        if element not in counted:
        #    print element
            number = 1
            i = 0
            while i < len(some):
                if element == some[i]:
                    if i < len(some)-1:
                        if some[i] == some[i+1]:
                            number = number + 1
                        else:
                            break
                    else:
                        break
                i = i + 1

            counted.append(element)
            if number > max:
                longest = element
                max = number
    return longest












#For example,

print longest_repetition([1, 2, 2, 3, 3, 3, 2, 2, 1])
# 3

print longest_repetition(['a', 'b', 'b', 'b', 'c', 'd', 'd', 'd'])
# b

print longest_repetition([1,2,3,4,5])
# 1

print longest_repetition([])
# None

print longest_repetition([[1], [2, 2], [2, 2], [2, 2], [3, 3, 3]])




