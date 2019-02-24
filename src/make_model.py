from .support import fallback


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
    
    maker = fallback(
        *[switch[data_type] for data_type in data_types],
    )
    
    return maker(schema)
    

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
            
    return types
         
def merge_properties(schema):
    properties = []
    
    schemas = schema.get('anyOf', []) or \
        schema.get('allOf', []) or \
        schema.get('oneOf', []) or \
        [schema]
    
    for schema in schemas:
        if 'properties' in schema:
            types += schema['properties']
            
    return properties
    
make_string = lambda schema: lambda value: string_validation(schema, value) and str(value)

make_number = lambda schema: lambda value: number_validation(schema, value) and value

make_boolean = lambda schema: lambda value: number_validation(schema, value) and value

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
    lambda value: array_validation and \
    fallback(
        lambda: [make_model(schema.get('items', {}))(**v) for v in value],
        lambda: [make_model(schema.get('items', {}))(v) for v in value],
    )()


def number_validation(schema, value):
    if not isinstance(v, int) and not isinstance(v, float):
        raise ValueError(
                'The attribute "{0}" must be an int or float, but was "{1}"'.format(k, type(value)))
    
    return True

def string_validation(schema, value):
    if type_ == 'string' and not isinstance(v, str):
        raise ValueError('The attribute "{0}" must be a string, but was "{1}"'.format(k, type(value)))
    
    return True
        

def boolean_validation(schema, value):
    if type_ == 'boolean' and not isinstance(v, bool):
        raise ValueError('The attribute "{0}" must be an int, but was "{1}"'.format(k, type(value)))
    
    return True


def array_validation(schema, value):

    if not isinstance(value, (list, tuple,)):
        raise ValueError('The attribute "{0}" must be an array, but was "{1}"'.format(k, type(value)))
    
    return True


def object_validation(schema, **kwargs):
        
    for k, v in kwargs.items():
    
        if k not in schema.get('properties', {}):
            raise ValueError(
                    'The model "{0}" does not have an attribute "{1}"'.format(self.__class__.__name__, k))
                    
    for key in schema.get('required', []):
        if key not in kwargs:
            raise ValueError('The attribute "{0}" is required'.format(key))

            
    return True

    
class Object:
    
    __setitem__ = object.__setattr__
    
    __getitem__ = object.__getattribute__ 
    
    __delitem__ = object.__delattr__
    
    __slots__ = tuple()
    
    _schema = {}

    def __init__(self, **kwargs):
        
        schema = self._schema
        
        assert object_validation(schema, **kwargs)
        
        properties = schema.get('properties', {})
        
        for k, v in kwargs.items():
                        
            fallback(
                lambda: setattr(self, k, make_model(schema=properties[k])(**v)),
                lambda: setattr(self, k, make_model(schema=properties[k])(v)),
            )()
            
            
        
                
                

