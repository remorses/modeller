from .make_model import make_model
import json


schema = json.load(open('src/test.json'))


        
    

Model = make_model(schema=schema)



data = {
    'billing_address': {
        'street_address': 'ciao',
        'state': 'usa',
        'city': 'sd'
        'code': 'boh',
    },
    'shipping_address': {
        'street_address': 'asd',
        'state': 'usa',
        'city': 'boh',
    }
}

somewhere = Model(**data)

print(somewhere)
print(somewhere.billing_address)
print(somewhere.billing_address.code)