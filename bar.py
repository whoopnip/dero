
from functools import partial

class Bar:

    def bar1(self):
        return 5

    def bar2(self):
        x = self.bar1()
        return 6
    
def bar3(x):
    return 7 + x

bar4 = partial(bar3, 5)