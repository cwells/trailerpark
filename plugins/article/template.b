div (class_='post') [
    h2 [ a (href="/%(_id)s" % v.article) [ v.article ['title'] ] ],
    p [ render_article_body (v.article ['content']) ]
]


