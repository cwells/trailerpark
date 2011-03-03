import logging 

import tornado.web
from tornado.web import _utf8
from tornado import httpclient, httputil
from tornado.options import options

import trombi
import breve
from breve.tags.html import tags as T

from libs.plugin import Plugins, PluginTemplateLoader

# plugins = Plugins ()
breve.register_global ('plugin_loader', PluginTemplateLoader ())

breve.register_global ('config', {
    'blog_url': options.url,
    'blog_title': options.title,
    'blog_description': options.description,
    'blog_author': options.author
})


def Template ():
    return breve.Template (T, options.templates)


def allow_any (*privileges):
    """returns a decorator that authorizes an OR joined list:

    @allow_any ('admin', 'manager')
    """
    def decorator (method):
        @functools.wraps (method)
        def wrapper (self, *args, **kwargs):
            try:
                for p in privileges:
                    if self.current_user.get (p, False):
                        return method (self, *args, **kwargs)
                raise UserError (403, 'You must have %s privileges to do that.' % ' or '.join (privileges))
            except AttributeError:
                raise UserError (401, 'You are not logged in.')
        return wrapper
    return decorator


class UserError (tornado.web.HTTPError):
    def __init__ (self, status_code, user_message, log_message=None, *args):
        tornado.web.HTTPError.__init__ (self, status_code, log_message, *args)
        self.user_message = user_message

    def __str__ (self):
        return self.user_message


class Aggregator (object):
    '''used as a callback that accumulates results of multiple
    separate callbacks and finishes when they are all accounted for
    '''
    def __init__ (self, finish, required):
        '''finish is a callback function to be invoked when all required callbacks are done
        required is a list of names of callbacks (strings)
        '''
        self.finish = finish
        self.required = required
        self.values = { }

    def __call__ (self, which, values, mapper=None):
        if mapper:
            values = map (mapper, values)
        self.values [which] = values 
        if set (self.required) == set (self.values.keys ()):
            self.finish (self.values)

    def __add__ (self, required):
        self.required.append (required)
        return self


class BaseHandler (tornado.web.RequestHandler):
    @classmethod
    def dbcallback (cls, db):
        cls.couchdb = db
        cls.plugins = Plugins (db)
        breve.register_global ('plugins', cls.plugins)

    def initialize (self, *args, **kw):
        self._args = kw

        # check for special form variable to indicate an 
        # alternate HTTP method because HTML sucks.
        self.request.method = self.get_argument ('.method', self.request.method)


server = trombi.Server ('http://%s:%s' % (options.couch_host, options.couch_port))
server.get (options.couch_db, BaseHandler.dbcallback, create=options.install)
