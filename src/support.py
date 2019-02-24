from collections.abc import Mapping

def expandable(value):
    if isinstance(value, Mapping):
        return True
    else:
        return False 


def fallback(*approaches):
    """Tries several approaches until one works.
       Each approach has a form of (callable, expected_errors)."""
    for approach in approaches:
        func, catch = (approach, Exception) if callable(approach) else approach
        catch = _ensure_exceptable(catch)
        try:
            return func()
        except catch:
            pass

def _ensure_exceptable(errors):
    """Ensures that errors are passable to except clause.
       I.e. should be BaseException subclass or a tuple."""
    is_exception = isinstance(errors, type) and issubclass(errors, BaseException)
    return errors if is_exception else tuple(errors)
