'''Enables markdown as well as source code colorizing via pygments
'''

target    = None
css       = ['pygments.css', 'style.css']
macros    = []
templates = []
js        = []
views     = []


import breve
import markdown

# if there's an existing render_article_body(), save it
_render_article_body = breve.globals.get_globals ().get ('render_article_body', str)

md = markdown.Markdown (
        extensions=['codehilite', 'footnotes'], 
        # extension_configs={'footnotes' : ('PLACE_MARKER','~~~~~~~~')},
        # safe_mode=True,
        output_format='xhtml'
)

def markdown2html (content):
    if not content.startswith ('<!-- format: markdown -->'):
        return _render_article_body (content)

    return breve.tags.xml (
        md.convert (content)
    )

breve.register_global ('render_article_body', markdown2html)
