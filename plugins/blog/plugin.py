''' this plugin defines the schema and API for a blog
'''

depends  = ['theme']
provides = 'blog'
macros   = ['macros']
install  = {
    "views": {
        "articles_by_date": {
            "map": "function(doc) { if (doc.date) emit(doc.date, doc); }"
        }
    }
}


import breve

_render_article_body = breve.globals.get_globals ().get ('render_article_body', str)
breve.register_global ('render_article_body', _render_article_body)


