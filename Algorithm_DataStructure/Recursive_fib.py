def get_fib(position):
    first,second = 0, 1
    for fib_pos in range(position - 1):
        first,second = second,first + second

    return second

def get_fib_recursive(position):

    if position == 0:
        return 0
    elif position == 1:
        return 1
    elif position >= 2:
        return get_fib_recursive(position - 1) + get_fib_recursive(position - 2)

    return -1

print get_fib(4)
print get_fib_recursive(2)