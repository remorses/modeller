

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
