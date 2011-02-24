div (id='editor') [
    form (target='') [
        fieldset [
            legend [ "Article" ],
            ol [
                li [
                    label (for_="title") [ "Title" ],
                    input (id="title", style="width: 100%;", value=v.article ['title'])
                ],
                li [
                    label (for_="summary") [ "Summary" ],
                    textarea (id="summary", style="width: 100%; height: 4em;") [
                        v.article ['summary']
                    ]
                ],
                li [
                    label (for_="content") [ "Content" ],
                    textarea (id="content", style="width: 100%; height: 30em;") [ 
                        v.article ['content'] 
                    ]
                ],
                li [
                    label (for_='published') [ 'Published' ],
                    checkbox (name="published", checked=v.article ['published']) 
                ]
            ]
        ]
    ]
]

