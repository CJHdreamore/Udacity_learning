# This is collections of errors & explaination

# Statement: "Object is not callable."
# Situation:  I met this when I def the class of stack.
#             In order to return the top element of the stack, I define a 'function' called [top]
#             However, I negelect that in the previous __init__(self,size),I already def a variant called self.top
#             Therefore, there are two concepts both called top,one is the previous variant,the later is the function name.
#             The reptition makes error: Object is not callable.
#             It's the repetition of def makes the error!
# 2017.5.23

