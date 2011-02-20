'''Uses jflickrfeed and jquery to display a flickr feed.
See http://www.gethifi.com/blog/a-jquery-flickr-feed-plugin for details.
You can obtain your flickr user ID at http://www.flickr.com/services/api/explore/?method=flickr.photos.getAllContexts
'''

settings = {
    'user_id': '30531103@N00',
    'thumb_count': 6
}

target    = 'sidebar'
depends   = ['jquery']
js        = ['jflickrfeed.min.js']
css       = ['style.css']
templates = ['template']

import breve
breve.register_global ('flickr_data', settings)
