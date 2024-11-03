class kkk:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def execute(self, func, **kwargs):
        print(func(self.a, self.b, **kwargs))
def add(a,b,z):
    print(z)
    return a + b 

m = kkk(5,7)
m.execute(add, z= "hej")