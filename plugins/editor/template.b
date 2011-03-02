div (id='editor') [
    form (action='/edit/article/%s' % v.article.id, method='POST') [
        input (type='hidden', name='.redirect', value='/view/article/%s' % v.article.id),
        fieldset [
            legend [ "Article" ],
            ol [
                li [
                    label (for_="title") [ "Title" ],
                    input (type='text', name="title", style="width: 100%;", value=v.article ['title'])
                ],
                li [
                    label (for_="summary") [ "Summary" ],
                    textarea (name="summary", style="width: 100%; height: 4em;") [
                        v.article ['summary']
                    ]
                ],
                li [
                    label (for_="content") [ "Content" ],
                    textarea (name="content", style="width: 100%; height: 30em;") [ 
                        v.article ['content'] 
                    ]
                ],
                li [
                    label (for_='published') [ 'Published' ],
                    checkbox (name="published", checked=v.article ['published']) 
                ],
                li [
                    label (for_='featured') [ 'Featured' ],
                    checkbox (name="featured", checked=v.article ['featured']) 
                ],
                li (class_='buttons') [
                    input (type_='submit', name=".save", value="save"),
                    input (type_='reset', name=".reset", value="reset")
                ]
            ]
        ]
    ]
]

