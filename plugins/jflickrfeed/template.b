inlineJS ('''
    $(document).ready (function () {
        $('#flickr').jflickrfeed ({
	    limit: %(thumb_count)s,
	    qstrings: {id: '%(user_id)s'},
	    itemTemplate: '<a href="{{image_b}}" rel="facybox"><img src="{{image_s}}" alt="{{title}}" /></a>'
        });
    });
''' % flickr_data),

div ( class_="box" ) [
    h2 [ "Flickr Photos" ],
    div ( id='flickr' )
]


