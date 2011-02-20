''' this plugin defines the schema and API for a blog
'''

from datetime import datetime
import logging
from tornado.options import options
import breve

today = datetime.today ().strftime ('%Y/%m/%d') # used in welcome doc

depends  = ['installer', 'theme']
provides = 'blog'
macros   = ['macros']
install  = {
    "views": {
        "articles_by_date": {
            "map": "function(doc) { if (doc.date) emit(doc.date, doc); }"
        }
    },

    "docs": [
        { "_id": "%s/welcome" % today,
          "title": "Welcome!",
          "content": '.. format: rst\n\nWelcome to %s_. \n\n.. _%s: %s' % (options.title, options.title, options.url),
          "tags": "",
          "date": today,
          "thumb": "/images/categories/servers.jpg",
          "category": "",
          "featured": True,
          "featured_image": "/images/featured/datacenter.jpg",
          "summary": "Welcome to PostBlog!" }
    ]
}

_render_article_body = breve.globals.get_globals ().get ('render_article_body', str)
breve.register_global ('render_article_body', _render_article_body)
