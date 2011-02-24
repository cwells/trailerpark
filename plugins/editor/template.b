div (id='editor') [
    form (target='') [
        fieldset [
            legend [ "Article" ],
            ol [
                li [
                    label (for_="title") [ "Title" ],
                    input (id="title", style="width: 100%;")
                ],
                li [
                    label (for_="summary") [ "Summary" ],
                    textarea (id="summary", style="width: 100%; height: 4em;")
                ],
                li [
                    label (for_="content") [ "Content" ],
                    textarea (id="content", style="width: 100%; height: 30em;")
                ],
                li [
                    fieldset [
                        legend [ "Published" ],
                        label [ input (type="radio", name="published") [ "Yes" ] ],
                        label [ input (type="radio", name="published") [ "No" ] ]
                    ]
                ]
            ]
        ]
    ]
]
