div (class_='post') [(
    h2 [ a (href="/%(_id)s" % v.article) [ v.article ['title'] ] ],
    p [ render_article_body (v.article ['content']) ]
) if not isinstance (v.article, Exception) else (
    div (style='text-align: center; width: 100%;') [ 
        h2 [ "Oops." ],
        p [ str (v.article) ] 
    ]
)]


