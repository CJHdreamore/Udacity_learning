from pandas import  DataFrame,Series
import numpy
d = {'one':Series([1,2,3],index = ['a','b','c']),
     'two':Series([1,2,3,4],index=['a','b','c','d'])
     }
df = DataFrame(d)
print df
print ''
print df.apply(numpy.mean)
print ''
print df['one'].map(lambda x:x>=1)
print ''
print df.applymap(lambda  x:x>=1)
