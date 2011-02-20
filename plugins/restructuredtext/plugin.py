'''Enables restructuredText as well as source code colorizing via pygments
'''

target    = None
css       = ['pygments.css', 'rest.css']
macros    = []
templates = []
js        = []
views     = []
depends   = []

import breve

from docutils.core import publish_parts
from docutils import nodes
from docutils.parsers.rst import directives

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

PYGMENTS_FORMATTER = HtmlFormatter ()
def pygments_directive (name, arguments, options, content, lineno,
                        content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name (arguments [0])
    except ValueError:
        # no lexer found
        lexer = get_lexer_by_name ('text')
    parsed = highlight (u'\n'.join (content), lexer, PYGMENTS_FORMATTER)
    return [ nodes.raw (u'', parsed, format = 'html')]

pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
directives.register_directive ('sourcecode', pygments_directive)


# if there's an existing render_article_body(), save it
_render_article_body = breve.globals.get_globals ().get ('render_article_body', str)

def rst2html (content):
    if not content.startswith ('.. format: rst'):
        return _render_article_body (content)

    return breve.tags.xml (
        publish_parts (
            content, 
            writer_name="html",
            settings_overrides = { 
                'halt_level': 6,
                'file_insertion_enabled': 1,
                'raw_enabled': 1 
            }
        )["html_body"]
    )

breve.register_global ('render_article_body', rst2html)
