macro ('featured_image', lambda _i, _a:
    div (id="fragment-%s" % _i, class_="ui-tabs-panel%s" % ("", " ui-tabs-hide")[_i > 1]) [
        img (src=_a ['featured_image']),
        div (class_="info") [
            h2 [ a (href="#") [ _a ['title'] ] ],
            p [
                _a ['summary'], br,
                a (href="#") [ 'read more' ]
            ]
        ]
    ]
),

macro ('featured_nav', lambda _i, _a:
    li (class_="ui-tabs-nav-item %s" % ('ui-tabs-selected', '')[_i > 1], id="nav-fragment-%s" % _i) [
        a (href="#fragment-%s" % _i) [
            img (src='/images/featured/image%s-small.jpg' % _i, alt=""),
            span [ _a ['title'] ],
        ]
    ]
),

div ( id_="featured" ) [
    [ featured_image (_i + 1, _a ['value']) 
      for _i, _a in enumerate (v.featured_articles ['rows']) ],

    ul (class_="ui-tabs-nav") [
        [ featured_nav (_i + 1, _a ['value']) 
          for _i, _a in enumerate (v.featured_articles ['rows']) ]
    ]
]
