# In C, we can use struct (array + integer_index)
#              or  struct ( linklist) + array_ptr
# to construct a tree

#In phython,we can do it easily. Using a nested list   [well,maybe not so easily.]
# Remember that list in python is somehow like the struct in C
# It's not surprising we can build a tree through list.

mytree = ['a', ['b', ['d',[],[]],['e',[],[]] ],['c',['f',[],[]] ] ]

print mytree

print('left subtree =',mytree[1])
print('root = ',mytree[0])
print('right subtree =',mytree[2])


