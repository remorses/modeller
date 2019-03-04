if __name__ == '__main__':
    import yaml
    import json
    # from memory_profiler import profile

    # @profile
    def main():
        import modeller

        class X:
            pass

        class User(X, modeller.Model):
            _schema = {
                'type': 'object',
                'properties': {
                    'name': { 'type': 'string' },
                    'id': { 'type': 'string' },
                    'age': { 'type': 'integer' },
                    'obj': {
                        'type': 'object',
                        'properties': {
                            'hey': {}
                        }
                    },
                    'arr': {
                        'type': 'array',
                    }
                },
                'required': [
                    # 'name',
                    # 'surname',
                ],
                # 'additionalProperties': False,
            }

        me = User(id='Tommy',name='Tommy', surname='Der', external=0 )

        another = User( )

        # me.ciao = 'fg'
        #
        # me.h = 9

        print(me._yaml())

        print(another.id)

        # me._validate()
    main()
