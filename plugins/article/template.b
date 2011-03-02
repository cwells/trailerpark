div (class_='post') [(
    h2 [ a (href="/view/article/%s" % v.article.id) [ v.article ['title'] ] ],
    p [ render_article_body (v.article ['content']) ],
    p [ a (href="/edit/article/%s" % v.article.id) ['Edit'] ]

) if not isinstance (v.article, Exception) else (
    div (style='text-align: center; width: 100%;') [ 
        h2 [ "Oops." ],
        p [ str (v.article) ] 
    ]
)]


