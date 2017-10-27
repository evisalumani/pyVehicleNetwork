import functools
class A:
    def __init__(self, _a, _meh):
        self.a = _a
        self.meh = _meh

class B:
    def __init__(self, _b, _a_list):
        self.b = _b
        self.a_list = _a_list

class Merged:
    def __init__(self, _b, _a):
        self.b = _b
        self.a = _a

    def to_dict(self):
        return {
            "a": self.a,
            "b": self.b
        }
a1 = A("a1", "meh1")
a2 = A("a2", "meh2")
a3 = A("a3", "meh3")
a4 = A("a4", "meh4")
b1 = B("b1", [a1, a2])
b2 = B("b2", [a3, a4])
data = [b1, b2]

def map_rt_data(x):
    # the_a_s = list(map(map_a, x.a_list))
    the_a_s = [map_a(a) for a in x.a_list]
    return [map_to_merged(a, x.b) for a in the_a_s]

def map_a(x):
    return {"a": x.a}

def map_to_merged(a, b):
    return Merged(a['a'], b)

test = list(map(map_rt_data, data))
#TODO: flatmap the tests
test_reduced = functools.reduce(list.__add__, test)
# print(test[0][0].to_dict())
# print(test[0][1].to_dict())
print(test_reduced)
print(test_reduced[0].to_dict())