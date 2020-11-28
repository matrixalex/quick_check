from functools import wraps


def base_decorator(func):
    @wraps
    def cover(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(repr(e))
    return cover
