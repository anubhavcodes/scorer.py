import functools, logging

class log(object):
    ENTRY_MESSAGE = 'Entry Point for {}()'
    EXIT_MESSAGE = '{}() returned value {}'
    
    def __init__(self):
        self.logger = None
    
    def __call__(self, func):
        self.logger = logging.getLogger(func.__module__ + "." +func.__name__)
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__))  
            f_result = func(*args, **kwds)
            self.logger.info(self.EXIT_MESSAGE.format(func.__name__,f_result)) 
            return f_result
        return wrapper