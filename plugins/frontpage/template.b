macro ('show_article', lambda _i, _article:
    div (class_=('post', 'first post')[_i==0]) [
        h2 [ a (href="/%s" % _article ['_id']) [ _article ['title'] ] ],
        p [ render_article_body (_article ['content']) ]
    ]
),

[ show_article (_i, _a ['value']) 
  for _i, _a in enumerate (v.articles_by_date ['rows']) ]



