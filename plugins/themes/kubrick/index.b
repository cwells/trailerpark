# include global macros.  this is required.
[ include (plugins.macros (_plugin), loader=plugin_loader) 
  for _plugin in plugins.index (v.current_page) ],

html [
    head [
        title [ config ['blog_title'] ],
        
        include_css (),
        include_js (),

        style (type="text/css") [ '''
            #logo { margin: 0; padding: 0; }
        ''' ]
    ],
    
    body [
        div (id_="page") [
            div (id_="header") [
                div (id_="headerimg") [
                    h1 [ 
                        a (href_="/") [
                            img (id="logo", src="/images/trailerpark.png"), 
                            config ['blog_title']
                        ] 
                    ],
                    div (class_="description") [ config ['blog_description'] ]
                ]
            ],

            div (id_="banner") [
                include_plugins ('banner')
            ],

            div (id_="content", class_="narrowcolumn") [
                include_plugins ('content')
            ],
            
            div (id_="sidebar") [
                include_plugins ('sidebar', wrapper=lambda: div (class_='plugin'))
            ],

            div (id="footer") [
                p [ 'Copyright ', E.copy, ' 2011, %(blog_author)s. All rights reserved.' % config]
            ]
        ]
    ]
]
