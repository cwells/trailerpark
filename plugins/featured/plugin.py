'''A plugin to display featured posts using a slideshow.
'''

depends   = ['jquery', 'article']
css       = ['plugin.css']
js        = ['scripts.js']
templates = ['template']
views     = ['featured_articles']
install   = {
   'views': {
        'featured_articles': { "map": "function(doc) { if (doc.featured && doc.date) emit(doc.date, doc); }" }
    }
}
