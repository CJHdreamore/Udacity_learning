import sys

def mapword(w):
    print '%s\t%d'%(w,1)

m = []

for line in sys.stdin:
    line = line.strip()

    word,count = line.split('\t')
    m.append((word,count))

m = sorted(m)
for i in m:
    print '%s\t%s'%i
