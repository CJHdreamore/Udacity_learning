import re,collections

def words(text):
    return re.findall('[a-z]+',text.lower()) #re.findall(pattern,string,flags=0)
                                              # text.lower() transfer alphbet into lower

def train(features):
    model = collections.defaultdict(lambda:1) # the frequency of each word defult to be 1
    for f in features:
        model[f] += 1
    #print model
   # print isinstance(model,collections.defaultdict)
    return model             # model is returned as a new dictionary-like object
                             # type of model is collections.defaultdict
                             # it's a dictionary with initial value



NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits = [(word[:i],word[i:]) for i in range(len(word)+1)]
    #input: 'abc'-- string
    #output: [('','abc'),('a','bc'),('ab','c'),('abc','')]
    deletes = [a+b[1:] for a,b in splits if b]
    # input: 'abc'
    #output: [bc','ac','ab']

    transposes = [a + b[1] + b[0] + b[2:] for a,b in splits if len(b)>1]
    #output: ['acb','bca']

    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]

    inserts = [a + c + b for a, b in splits for c in alphabet] #this is easy

    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]

    return max(candidates,key=NWORDS.get)


print correct('korrecter')

print correct('speling')

print correct('ffive')
