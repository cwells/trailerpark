macro ('show_featured_photo', lambda _i, _feature:
    li (class_=['', 'first'][_i==0]) [ a (href="/%s" % _feature ['_id']) [ 
        img (src=_feature ['featured_image'], alt="") ] 
    ]
),

macro ('show_featured', lambda _i, _feature:
    li (class_=['', 'first'][_i==0]) [
        h2 [ a (href="/%s" % _feature ['_id']) [ _feature ['title'] ] ],
        p [ _feature ['summary'] ],
        a (href="/%s" % _feature ['_id'], class_="readmore") [ "Read Full Story" ]
    ]     
),

( # only renders if there are docs returned flagged 'featured'
    div (id="featured") [
        div (class_="featured_thumb") [
            div (class_="featured_content") [
                ul (class_="featured_photo") [
                    [ show_featured_photo (_i, _f ['value']) 
                      for _i, _f in enumerate (v.featured_articles) ]
                ],
                ul (class_="featured_text") [
                    [ show_featured (_i, _f ['value']) 
                      for _i, _f in enumerate (v.featured_articles) ]
                ]
            ]
        ] 
    ] 
) if 'rows' in v.featured_articles else ''
