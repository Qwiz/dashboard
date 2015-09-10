from functools import wraps
from app import app

def jinja_filter(param_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            app.jinja_env.filters[param_name] = func
            return func(*args, **kwargs)
        return wrapper
    return decorator
