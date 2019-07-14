
from typing import NamedTuple
from collections import namedtuple


class Undefined:
    __repr__ = lambda _: 'Undefined'
    pass

class Employee(NamedTuple):
    schema = """
    Employee:
        name: Str
        id: Int
    """
    name: str
    id: int

    @classmethod
    def make(cls, x, default=Undefined()):
        obj = {k: v for k, v in x.items() if k in cls._fields}
        misses = set(cls._fields) - set(obj.keys())
        [obj.update({miss: default}) for miss in misses]
        return cls(**obj)




x: Employee = Employee(name='a', id='c',)

y = Employee.make({'name': 'dsf', 'id': 0, 'shit': 6})

z = Employee.make({})
print(z)


name, id = y
print(name, id)

print(x._fields)
print(dir(x))




# print(x.__annotations__)





