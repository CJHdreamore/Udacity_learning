def quicksort(array):
    # convention select
    head = 0
    n = len(array)
    if n > 1:
        pivot_index = n - 1
        pivot = array[pivot_index]
    else:
        pivot = array[0]

    if n == 1:
        return array
    elif n > 1:
        while head < pivot_index:

            if array[head] > pivot:
                array[pivot_index] = array[head]
                array[head] = array[pivot_index - 1]
                pivot_index -= 1
                array[pivot_index] = pivot
            elif array[head] <= pivot:
                head += 1

    lower_array = array[0:pivot_index]
    higher_array = array[pivot_index:]
    return quicksort(lower_array) + quicksort(higher_array)

test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
print quicksort(test)