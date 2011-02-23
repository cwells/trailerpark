macro ('recent_articles_item', lambda _i:
    li (class_="page_item")[ a (href="/view/%(_id)s" % _i) [ _i ['title'] ] ]
)

