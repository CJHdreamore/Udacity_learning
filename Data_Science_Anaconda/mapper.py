import  sys

def mapword(w):
    print '%s\t%d'%(w,1)

for line in sys.stdin:
    line = line.strip()

    words = line.split()

    m = map(mapword,words)
