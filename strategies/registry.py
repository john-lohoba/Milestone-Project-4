from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

def load_strategy_class(python_path: str):
    """
    Load a Backtesting.py strategy class from a python import path stored in the DB.
    """
    try:
        StrategyClass = import_string(python_path)
    except Exception as exc:
        raise ImproperlyConfigured(
            f"Could not import strategy class '{python_path}': {exc}"
        )
    
    if not isinstance(StrategyClass, type):
        raise ImproperlyConfigured(
            f"Imported object '{python_path}' is not a class."
        )
    
    required_attrs = ["init", "next"]
    for attr in required_attrs:
        if not hasattr(StrategyClass, attr):
            raise ImproperlyConfigured(
                f"Imported strategy '{python_path}' is missing requiered method '{attr}'."
            )
        
        return StrategyClass