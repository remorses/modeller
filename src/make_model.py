from .support import fallback, merge
from jsonschema import validate, Draft7Validator


Validator = Draft7Validator


def make_model(
    schema: dict,
    name: str = 'Model',
    immutable: bool = False,
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
    schema['title'] = schema.get('title', '').replace(' ','_') or name
    
    switch = {
        'object':  make_object,
        'array':   make_array,
        'number':  make_number,
        'string':  make_string,
        'boolean': make_boolean,
    }
    
    data_types = merge_types(schema)
    
    print(data_types)
    
    maker = fallback(
        *[lambda: switch[data_type](schema) for data_type in data_types],
    )
    
    print([switch[data_type](schema) for data_type in data_types])

    # print([switch[data_type](schema)(name='') for data_type in data_types])
    
    print(maker)
    
    return maker()
    

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
         
def merge_properties(schema):
    properties = {}
    
    schemas = schema.get('anyOf', []) or \
        schema.get('allOf', []) or \
        schema.get('oneOf', []) or \
        [schema]
    
    for schema in schemas:
        if 'properties' in schema:
            for k, v in schema['properties'].items():
                try:
                    merge(properties, {k:v})
                except:
                    raise
            
    return properties
    
make_string = lambda schema: lambda value: Validator(schema).is_valid(value) and str(value)

make_number = lambda schema: lambda value: Validator(schema).is_valid(value) and value

make_boolean = lambda schema: lambda value: Validator(schema).is_valid(value) and value

make_object = lambda schema: type(
    schema.get('title', 'Object'),
    (Object,),
    make_object_attributes(schema),
)

def make_object_attributes(schema):

    properties = merge_properties(schema)
    
    return {
        '__slots__': tuple(properties.keys()),
        '_schema': schema,
    }

make_array = lambda schema: \
    lambda value: Validator(schema).is_valid(value) and \
    fallback(
        lambda: [make_model(schema.get('items', {}))(**v) for v in value],
        lambda: [make_model(schema.get('items', {}))(v) for v in value],
    )()


def format_slots(self):
    return f"({', '.join([k + '=' + self[k] for k in self.__slots__ if k in self])})"

    
class Object:
    
    __setitem__ = object.__setattr__
    
    __getitem__ = object.__getattribute__ 
    
    __delitem__ = object.__delattr__
    
    __repr__ = lambda self: f'{self.__class__.__name__}({format_slots(self)}'
    
    __slots__ = tuple()
    
    _schema = {}

    def __init__(self, **kwargs):
        
        schema = self._schema
        
        Validator(schema).validate(kwargs)
        
        properties = schema.get('properties', {})
        
        for k, v in kwargs.items():
                        
            fallback(
                lambda: setattr(self, k, make_model(schema=properties[k])(**v)),
                lambda: setattr(self, k, make_model(schema=properties[k])(v)),
            )()
            
            
        
                
                

