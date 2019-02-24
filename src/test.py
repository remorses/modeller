from .make_model import make_model
import json


schema = json.load(open('test.json))


        
    

Model = make_model(schema=schema)



data = {
    'billing_address': {
        'street_address': 'ciao',
        'state': 'usa',
        'code': 'boh',
    }
    'shipping_address': {
        'street_address': 'asd',
        'state': 'usa',
        'code': 'boh',
    }
}

somewhere = Model(**data)

print(somewhere)
print(somewhere.billing_address)
print(somewhere.billing_address.code)