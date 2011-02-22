macro ('show_featured_photo', lambda _i, _feature:
    li (class_=['', 'first'][_i==0]) [ a (href="/%s" % _feature ['value']['_id']) [ 
        img (src=_feature ['value']['featured_image'], alt="") ] 
    ]
),

macro ('show_featured', lambda _i, _feature:
    li (class_=['', 'first'][_i==0]) [
        h2 [ a (href="/%s" % _feature ['value']['_id']) [ _feature ['value']['title'] ] ],
        p [ _feature ['value']['summary'] ],
        a (href="/%s" % _feature ['value']['_id'], class_="readmore") [ "Read Full Story" ]
    ]     
),

div (class_="featured") [
    h2 (class_="title") [ "Featured Posts" ],
    div (class_="thumb") [
        div (class_="b") [
            ul (class_="photo") [
                [ show_featured_photo (_i, _f) 
                  for _i, _f in enumerate (v.featured_articles ['rows']) ]
            ],
            ul (class_="text") [
                [ show_featured (_i, _f) 
                  for _i, _f in enumerate (v.featured_articles ['rows']) ],
            ]
        ]
    ]
]
