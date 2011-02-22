macro ('show_article', lambda _i, _article:
    div (class_=('post', 'first post')[_i==0]) [
        h2 [ a (href="/%s" % _article ['_id']) [ _article ['title'] ] ],
        span (class_='tagline') [
            'posted on %(date)s in ' % _article, 
            a (href="/categories/%(category)s") [ '%(category)s' % _article ]
        ],
        p [ render_article_body (_article ['content']) ],

        p (class_='tags')[
            'tags:', [ a (href="/tags/%s" % _t)[ ' %s' % _t ] 
                       for _t in _article ['tags'] ]
        ]
    ]
),

[ show_article (_i, _a ['value']) 
  for _i, _a in enumerate (v.articles_by_date ['rows']) ]



