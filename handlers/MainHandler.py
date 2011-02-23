import logging
import tornado
from tornado.options import options
from handlers.BaseHandler import BaseHandler, Template, Aggregator

class RequestHandler (BaseHandler):
    @tornado.web.asynchronous
    def get (self, action='view', page=''):
        if self._args: # we hit the catch-all
            action = self._args.get ('action', action)
            page = self._args.get ('page', page)
            if 'status' in self._args:
                self.set_status (self._args ['status'])
            
        pageinfo = {
            'action': action,
            'page':   page
        }

        def render (values):
            if isinstance (values.get ('article', None), Exception):
                self.set_status (values ['article'].code)
                
            if options.debug:
                for k, v in values.items ():
                    if isinstance (v, Exception):
                        logging.error ('Failed to load document(s) for "%s": "%s"' % (k, v))
                
            t = Template ()
            values ['_pageinfo'] = pageinfo
            self.write (t.render (options.index, vars=values))
            self.finish ()

        if options.debug:
            logging.info ('GET: action: %s, page: %s' % (action, page))

        views = []
        for p in self.plugins.index (pageinfo):
            views.extend (self.plugins[p].views)
        views = set (views)
        ag = Aggregator (render, list (views))

        if page:
            ag += 'article'
            self.couchdb.get_doc (page, lambda values: ag ('article', values))

        for view in views:
            self.couchdb.view (options.couch_design, view, lambda values, view=view: ag (view, values), limit=5)
    

    @tornado.web.asynchronous
    def head (self, action='view', page=''):
        if self._args: # we hit the catch-all
            action = self._args.get ('action', action)
            page = self._args.get ('page', page)

        pageinfo = {
            'action': action,
            'page':   page
        }

        def render (values):
            if isinstance (values.get ('article', None), Exception):
                self.set_status (404)

            self.write ('') # HEAD shouldn't return a body
            self.finish ()

        if options.debug:
            logging.info ('HEAD: action: %s, page: %s' % (action, page))

        views = []
        ag = Aggregator (render, views)

        if page:
            ag += 'article'
            self.couchdb.get_doc (page, lambda values: ag ('article', values))
        
