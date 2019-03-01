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

