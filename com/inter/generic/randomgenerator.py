import string
import random

class randomstring:
    
    def __init__(self):
        lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(17)]
        str = "".join(lst)
        self.str = str
    



    

