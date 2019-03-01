if __name__ == '__main__':
    import yaml
    import json
    import modeler

    schema = yaml.load("""
    type: object
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
    """)

    # schema = json.load(open('tests/test.json'))

    User = modeler.make_model(schema=schema,)

    data = {
        'billing_address': {
            'street_address': 'ciao',
            'state': 'usa',
            'city': 'sd',
            'code': 'boh',
        },
        'shipping_address': {
            'street_address': 'asd',
            'state': 'usa',
            'city': 'boh',
        }
    }
    # me = Model(**data)
    me = User(name='Tommaso', surname='De Rossi', age=19)


    print(me._json())

    print()

    class User(modeler.Model):
        _schema = {
            'type': 'object',
            'properties': {
                'name': { 'type': 'string' },
                'ciao': { 'type': 'string' },
                'age': { 'type': 'integer' },
            },
            'required': [
                'name',
                'surname',
            ],
            # 'additionalProperties': False,
        }

    me = User(name='Tommy', surname='Der')

    print(me._json())
