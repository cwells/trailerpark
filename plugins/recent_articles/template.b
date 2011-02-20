macro ('recent_article_item', lambda _i:
    li [ a (href="/%(_id)s" % _i) [ _i ['title'] ] ]
),

div (id='recent_articles') [
    ul [ 
        [ recent_article_item (_i ['value'])
          for _i in v.articles_by_date ['rows'] ] 
    ]
]

