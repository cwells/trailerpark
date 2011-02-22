import logging
import tornado
from tornado.options import options
from handlers.BaseHandler import BaseHandler, Template, Aggregator

class PageHandler (BaseHandler):
    @tornado.web.asynchronous
    def get (self, page=''):
        def render (values):
            t = Template ()
            values ['current_page'] = page
            if options.debug:
                logging.info ('rendering %s' % (page or '/'))
            self.write (t.render (options.index, vars=values))
            self.finish ()

        views = []
        for p in self.plugins.index (page):
            views.extend (self.plugins[p].views)
        views = set (views)
        ag = Aggregator (render, list (views))

        if page:
            ag += 'article'
            self.couchdb.get_doc (page, lambda values: ag ('article', values))

        for view in views:
            self.couchdb.view (options.couch_design, view, lambda values, view=view: ag (view, values), limit=5)


