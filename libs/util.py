from functools import partial
from tornado.ioloop import IOLoop

def with_ioloop (func):
    '''decorator used to provide IOLoop during 
    --install when normal IOLoop isn't running
    '''
    def wrapper (*args, **kw):
        ioloop = IOLoop.instance ()
        ioloop.add_callback (partial (func, ioloop, *args, **kw))
        ioloop.start ()

    return wrapper

