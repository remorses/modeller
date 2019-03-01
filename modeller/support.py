import collections
from functools import wraps


def ignore(errors, default=None):
    """Alters function to ignore given errors, returning default instead."""
    errors = _ensure_exceptable(errors)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors:
                return default
        return wrapper
    return decorator


def silent(func):
    """Alters function to ignore all exceptions."""
    return ignore(Exception)(func)

def fallback(*approaches):
    """Tries several approaches until one works.
       Each approach has a form of (callable, expected_errors)."""
    for approach in approaches:
        func, catch = (approach, Exception) if callable(approach) else approach
        catch = _ensure_exceptable(catch)
        try:

            return func()
        except catch:
            # if catch == Exception: # not predicted
            #     traceback.print_exc()
            pass

def _ensure_exceptable(errors):
    """Ensures that errors are passable to except clause.
       I.e. should be BaseException subclass or a tuple."""
    is_exception = isinstance(errors, type) and issubclass(errors, BaseException)
    return errors if is_exception else tuple(errors)



def merge(a, b):
    result = dict()

    [result.update({x: dict(**a[x], **b[x])}) for x in set(a.keys()) & set(b.keys())
        if isinstance(a[x], dict) and isinstance(b[x], dict)]

    [result.update({x: [*a[x], *b[x]]}) for x in set(a.keys()) & set(b.keys())
        if isinstance(a[x], list) and isinstance(b[x], list)]

    [result.update({x: a[x] if x in a else b[x]}) for x in set(a.keys()) ^ set(b.keys() )]

    return result



def resolve_refs( spec, uri='', store={}):
    """Resolve JSON references in a given dictionary.

    OpenAPI spec may contain JSON references to its nodes or external
    sources, so any attempt to rely that there's some expected attribute
    in the spec may fail. So we need to resolve JSON references before
    we use it (i.e. replace with referenced object). For details see:

        https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-02

    The input spec is modified in-place despite being returned from
    the function.
    """

    resolver = None #jsonschema.RefResolver(uri, spec, store=store)

    def _do_resolve(node):
        if isinstance(node, collections.Mapping) and '$ref' in node:
            with resolver.resolving(node['$ref']) as resolved:
                return resolved
        elif isinstance(node, collections.Mapping):
            for k, v in node.items():
                node[k] = _do_resolve(v)
        elif isinstance(node, (list, tuple)):
            for i in range(len(node)):
                node[i] = _do_resolve(node[i])
        return node

    return _do_resolve(spec)


if __name__ == '__main__':
    import yaml

    schema = yaml.load("""
    properties:
        ciao:
            $ref: cosa
    type: object
    """)
    store = {'cosa': "type: string"}

    resolved = resolve_refs(schema, store=store)

    print(resolved)
