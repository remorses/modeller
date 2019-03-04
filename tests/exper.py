


class call:
    __init__ = lambda self, fun: setattr(self, 'function ', fun)
    __enter__ = lambda self: self.function()
    __exit__ = lambda self: None



(lambda: with call(lambda: 'ciao') as res res)()
