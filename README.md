

## Usage

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

you can load a model with automatic validation and efficent use of `__slots__`
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
