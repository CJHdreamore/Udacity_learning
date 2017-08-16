#  DATA STRUCTURE IN PYTHON
# Type 1 : Sequence --- list,tuple,range

# LIST: in a list,the element can be a string,an integer

list1 = ['we','are','together']
#print list1

list2= ['10','28']
#print list2

# list can be empty

list3 =[]
#print list3

# How can we act with a list?

# (1)  If I want to take out one of the element from the list

#It is just like the array in C, the indext of an array is
#starting from zero,show:
#print list1[0]  # the first element in list
#print list1[-1] # the last element in list
#print list1[0:-1] #however, the first to the penultimate element
#print list1[0:] #from the first to the end
#print list1[:]  # well, the same function
# we can conclude that taking out elements from a list,the expression
# will include the start number but not!!!! include the later one.

# (2) If I want to add,delete some element into or from the list?
#  First,is it possible? If so, how ?

# The answer: yes, we can change elements in a list,thanks!

emp = []
print emp
emp.append(1)
#print emp
emp.append([1]) # can I append a list into the list?
#print emp   # the recursive is successful!!!!
emp.append('haha') # what about a string?
print emp
#definitely yes! the elements in a list can contain integer,string
#at the same time, thus ,it is more likely a struct in C language.

#append only allows us to add element follwing the last place
# thus it can be used to construct a queue-adding action.Naturally.

#What's more, in C if we want to insert some element into a'linear
# list', no matter it's a arry or a linklist,we should take many steps
# like shift.

#However!!!! In python!!! If we want to assert an element into a list
# Simply we can use one function.

emp.insert(0,'in')
print emp
emp.insert(1,'again')
print emp
emp.remove('in') # delete one specific element
print emp
#emp.pop()  # remove the last element in list
#print emp
#emp.pop(2)  # pop can direct the inex of the element I want to pop
#print emp
#emp.remove(2)   # !!! remove cant indicate a place as pop does
#print emp      #otherwise,it's unnecessary to define two actions

#even some more inrooted actions
emp.append(1)
print emp.count(1)
print emp.index('again') # return the indext that the element occurred

# It seems I can insert any element into the list,and I dont worry
# about how big the list must be.
# In other word, it's the same as dynamic linklist in C

# So I can image using list I can achieve stack or queue !!!!

# logical structure: stack

# Take heed !!!!!!!!!!!!!
# list is a data type in python,just like a struct
# in C ,it belongs to sequence,it's special cause it can change its
#elements by various conduction.

#Based on list in python: [2,'dls',[1,'dsfd]], we can achieve many
#logical structure: stack queue .....

#There is another function called list,it results:

print list('dsfs')

# take every character from a string and use them to create a
# list,each element is the character of string.


# Interesting !!!!!! we can derive from a simple list

s = [2,4,6]
#r = [2*element for element in s if element <5]
#print r
u = [1,2,3]
print [x*y for x in s for y in u] #Amazing!!! it's not just
#  number's multiplication in correspondent place

# we can even use list to build a matrix

mat = [[1,2,3],
       [4,5,6],
       [7,8,9]]
print mat
print ([[row[i] for row in mat] for i in [0,1,2]])
# why this expression will output the column of this matrix?
# first, i is fixed to 0, and then row changes:row2[0],row1[0],
# row3[0])  so it's the first column.

print list(zip(mat))
print list(zip(*mat))  # this expression also output
                       # the column element of mat
                       # but one clumn is in a tuple,not a list

#Tuple: Why we need tuple?

# The first reason: tuples are used to store collections of heterogeneous data
# the 'heterogeneous' means enumerate --

seasons = ['Spring','Summer','Fall','Winter']  # this is a list
print list(enumerate(seasons))
# according to enumerate(),this function change a list into some tuples
# each two-element tuple concludes (#,'element' in the list)
# and list() collects those tuples into a list,each element of the list
# is a tuple.
print list(enumerate(seasons,start=1))

#The second reason: tuples are also used to store homogeneous data
# this is different from enumerate!!
# notable: tuple is different from list cause it's immutable.

# So,what's the meaning of immutable? why we distinguish immutable
# and mutable sequence?

# immutable in python means that : these objects are hashable!
# hashable indicates that these objects can be used as a key or
# a member of a set. Because they must have a unique hash value.

# So we can see,tuples and strings are immutable sequence,they
# can be used as a key,but list and dictionary are not hashable,
# they are mutable.

#create tuple
#if we simply write: t = 1,2,3 -- this means we create a tuple
t = 1,2,3
print t
#maybe more formal
t =(1,2,3)
print t
tt = (1,'2',3) # tuples can also contain integer& char at same time
print tt
# class tuple([iterable])-- turn a sequence into tuple
print tuple([1,2,3])
print tuple((1,2)) #the element is already a tuple
print tuple('likewise')
#The core for creating a tuple is the comma! we can neglect the ()





#Range: this is a sequence? somehow?

# range is immutable,it's totally for a 'for' loop!
# key points: contents must be integers
# if the content is negative integer,that means the loop starts
#from the last element,and is in a reverse order.

#format: range(start,stop,step)
print list(range(10)) # default:start from 0,till stop-1
print list(range(0,10))
print list(range(0,10,2))
print list(range(0,-10))  #compare with the next expression
print list(range(0,-10,-1))

#why range? tuple or list enough?
r = range(0,20,2) # in fact, it returns a list
10 in r # means 'True'.we can make this statement,sometimes as a condition
#print r.index(10)

#can you do the same thing in a tuple?
t = tuple(r)
print 10 in t # it seems we can ,but we start from using range
              # to make up this list,and then this tuple




# Text Sequence Type -- str!  it's natural
# string is immutable,it allows same conductions used in sequence
str = 'lalalandl'
print str + 'ing'

# I'd like to focus on the specific implement in string
print str.capitalize() # the opposite function str.lower()
print len(str)
print str.count('l',0,-1)
print str.find('l',1)
change = str.capitalize()
print change
print change.lower()

s = '     spacious    '
#notable! if just writes s.lstrip(),s doesn't change!!!
s = s.lstrip() # remove the whitespace
#print s.lstrip('ous') #lstrip just starts removing from
                       # the begining. different from remove in list
# if I really want to delete char from the rear,use:
print s.rstrip()
#strip returns a string while rsplit returns a list
print s.rsplit()

print s.partition('o')
# returns a 3-tuple

















































