
import jedi



source = '''
import json
json.l
'''

script = jedi.Script(source[1:], 2, 6, '')




source = '''
class User:
    __slots__ = ['ciao']
x = User()
x.
'''
script = jedi.Script(source[1:], 4, 2, '')
completions = script.completions()
print(completions)
print()

source = '''
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'],)
p = Point(x=1, y=2)
p.
'''
script = jedi.Script(source[1:], 4, 2, '')
completions = script.completions()
print(completions)
