provides  = 'featured'
depends   = ['theme', 'jquery', 'jquery-ui']
templates = ['template']
css       = ['style.css']
js        = ['featured.js']
views     = ['featured_articles']
install   = {
   'views': {
        'featured_articles': { "map": "function(doc) { if (doc.featured && doc.date) emit(doc.date, doc); }" }
    }
}
