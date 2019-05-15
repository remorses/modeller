from .support import fallback, merge, resolve_refs, silent
import fastjsonschema
import json
import sys



def make_model(
        schema: dict,
        name: str = 'Model',
        uri: str = '',
        store: dict = {},
        # immutable: bool = False,
    ):
    """
    import yaml

    schema = yaml.load(open('types/model.yml').read())

    Model = make_model(
        schema=schema,
        immutable=True,
        # set_defaults=True # if schema has a default and property is not presetn it will use the default value
    )
    """
    # if not schema:
    #     raise Exception('schema is needed to instantiate a model')

    uri = uri or schema.get('$id', '')

    schema = resolve_refs(schema, uri, store=store)

    if schema.get('type', '') == 'object':
        schema['title'] = schema.get('title', '') \
            .replace(' ','_') \
            .replace('.','_') \
            .replace('/','_') \
            .replace('-','_') or name


    # print('schema', schema)
    elastic_identity = lambda arg=None: arg

    switch = {
        'object':  make_object(schema),
        'array':   make_array(schema),
        'number':  elastic_identity,
        'integer':  elastic_identity,
        'string':  elastic_identity,
        'boolean': elastic_identity,
        'null': elastic_identity
    }

    data_types = merge_types(schema)

    # print(data_types)

    maker = fallback(
        *[(lambda: switch[data_type], TypeError) for data_type in data_types],
        lambda: elastic_identity
    )
    # print(maker)

    return maker


def merge_types(schema):
    types = []

    schemas = schema.get('anyOf', []) or \
        schema.get('allOf', []) or \
        schema.get('oneOf', []) or \
        [schema]

    for schema in schemas:
        if 'type' in schema:
            types += [schema['type']]

        elif any(x in schema for x in ('allOf', 'anyOf', 'oneOf')):
            types += merge_types(schema)

    return list(set(types))



make_string = lambda schema: lambda value: value

make_number = lambda schema: lambda value: value

make_boolean = lambda schema: lambda value: value

make_array = lambda schema: \
    lambda value=[]: fallback(
        (lambda: [make_model(schema.get('items', {}))(**v) for v in value], TypeError),
        (lambda: [make_model(schema.get('items', {}))(v) for v in value],TypeError),
    )

SENTINEL = 'not_found'



class Meta(type):
    def __new__(cls, name, bases, dct):
        # protected = ['id']
        # print('hey' in dct)
        slots = set(dct.get('_schema', {}).get('properties', {}).keys())  - set(dct.keys())
        dct.update({'__slots__': list(slots)})
        validate = fastjsonschema.compile(dct.get('_schema', {}))
        dct.update({'_validate': lambda self: validate(self._serialize())})
        x = super().__new__(cls, name, bases, dct)
        return x

def throw(e):
    raise e

def get_missing(self, name):
    subschema = self._schema.get('properties', {}).get(name, None)
    if subschema is not None:
        return make_model(subschema)()
    else:
        raise AttributeError(f'{name} not present')

class Model(dict, metaclass=Meta):

    __metaclass__ = Meta

    __setattr__ = dict.__setitem__

    __delattr__ = dict.__delitem__

    def __getitem__(self, name):
        try:
            val = object.__getattribute__(self, name)
        except:
            val = dict.get(self, name, SENTINEL)
            if val == SENTINEL:
                 subschema = self._schema.get('properties', {}).get(name, None)
                 if subschema is not None:
                     val = make_model(subschema)()
                 else:
                     raise
        return val

    __getattribute__ = __getitem__

    _validate = lambda: None

    _schema = {}

    def __init__(self, **kwargs):

        # print('__slot__', self.__slots__)
        # print('_schema', self._schema)

        schema = self._schema

        # print(kwargs)

        properties = schema.get('properties', {})

        for k in kwargs.keys():
            # print(k)
            v = kwargs.get(k)
            fallback(
                (lambda: setattr(self, k, make_model(schema=properties.get(k, {}))(**v)), TypeError),
                (lambda: setattr(self, k, make_model(schema=properties.get(k, {}))(v)), TypeError),
            )
            # print(k)
        self._on_init()

        # print(self.__additional__)

    _on_init = lambda self: self._validate()

    def _serialize(self):
        result = dict()
        for slot in self:
            # print(slot)
            value = self[slot]._serialize() if hasattr(self[slot], '_serialize') else self[slot]
            if value is not None:
                result[slot] = value
        return result


    def _json(self, indent=4):
        return json.dumps(self._serialize(), indent=indent)

    def _yaml(self, indent=4):
        if 'yaml' in sys.modules:
            yaml = sys.modules['yaml']

            class Dumper(yaml.Dumper):
                def increase_indent(self, flow=False, indentless=False):
                    return super(Dumper, self).increase_indent(flow, False)

            return yaml.dump(self._serialize(), Dumper=Dumper, default_flow_style=False)
        else:
            throw(Exception('import yaml before calling model._yaml()'))



def merge_properties(schema):
    properties = {}

    schemas = schema.get('anyOf', []) or \
        schema.get('allOf', []) or \
        schema.get('oneOf', []) or \
        [schema]

    for schema in schemas:
        if 'properties' in schema:
            for k, v in schema['properties'].items():
                properties = merge(properties, {k:v})
    return properties

make_object = lambda schema: type(
    schema.get('title', 'Object'),
    (Model,),
    {
        '__slots__': tuple(merge_properties(schema).keys()),
        '_schema': schema,
    },
)
