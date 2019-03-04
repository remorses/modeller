

## Usage

You can use inheritance to create your model:
```
class User(modeller.Model):
    id = ''
    _schema = {
        'type': 'object',
        'properties': {
            'name': { 'type': 'string' },
            'id': { 'type': 'integer' },
            'age': { 'type': 'integer' },
        },
        'required': [
            'name',
            'surname',
        ],
        # 'additionalProperties': False,
    }

# model will be validated after every instance
me = User(id=01, name='Tommy', surname='Der')

# you can also add additional properties
me.state = 'Italy'
me._validate()

print(me._json())

print(me._yaml())

print(me.surname)
```

With the schema in `types/schema.yaml`
```yaml
$schema: http://json-schema.org/schema#
properties:
  name:
    type: string
  surname:
    type: string
  age:
    type: integer
required:
  - name
  - surname
  - age
```

you can load a model with automatic validation, easy attribute access with dots and no exceptions while trying to access a property defined in the schema.

```python
import yaml
import modeler

schema = yaml.load(open('types/schema.yaml').read())

Model = modeler.make_model(schema=schema,)

Model(name='Tommaso', surname='De Rossi', age=19)
```


## Details

Model validate itself as soon as instantiated, if you want to change this behavior overwrite `_on_init` method.
Model will return None if you try to access a property present in the json schema `.properties` but not in the object.
Model will throw if you try to access a property not present in the object and not in the json schema `.properties`.
