# What's the definition of class in python?
# It is said that python is an objected-oreiented language,which shows that
#it can define class.

#If we define a class for an object, a class has some attributes. Then we can use the name
# of the class to visit its attributes.

#Whatever, let's see some examples.



#Exp1:

class people:
    # define its basical attributes
    name = ''    # this variant is directly defined in a class,namely CV
    age = 0
    # define some private attributes
    #private attributes cant be visited
    #if you are outside the class
    __weight = 0 # private attribute
    # construct funtion?
    def __init__(self,n,a,w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):  # this is method of a class;in fact we can def
                      # another variant in method,they are called MV
        print("%s is speaking: I am %d years old" %(self.name,self.age))


p = people('Tom',10,30)
p.speak()

# try to realize the meaning of class
# what's in a class?    there are some 'variant' -- name,age,__weight;
#                       there are some functions -- construct function: seems to transfer parameters into the 'variant
#                       a more specific function -- speak
#                       It seems that a class is not only defined some functions,it also concluded the variant suitbale for the
#                       function!

#Exp2:  Exp1 is simple,class people is somehow independent.

class student(people): # class_name(father_class_name)
    grade = ''
    def __init__(self,n,a,w,g):
        people.__init__(self,n,a,w)  # we can simply call the
                                     # construction function in father class
        self.grade = g
    def speak(self):
        print("%s is speaking: I'm %d years old,and I'm in grade %d "%(self.name,self.age,self.grade))

s = student('Ken',20,60,3)
s.speak()

#Exp3: In fact,a new class can heritate from several father class
# we can see in def__init__(self),we call from the father init


#Exp4: What's the meaning of 'if __name__ =='__main__':

# files in python are used in two ways:
#  1.they can run directly as scripts.
#  2.they can be imported by other files to run.

# using 'if __name__ == '__main__': the following codes will only be
# implemented in directly running, not in imported method.

# Why does this happen?

# In every .py,there is a in-builted variant -- __name__
# when .py is running, __name__ equals the file of the whole name(xx.py)
# if .py is imported into other files,__name__ equals only the identity(xx)
# while '__main__' == the file running currently(xx.py)

#Therefore, __name__ ='__main__' is ture only in the first way to run a file






