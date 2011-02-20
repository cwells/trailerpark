[ [ include (_tpl, loader=plugin_loader)
    for _tpl in plugins.macros (_plugin) ]
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

            div (id_="content", class_="narrowcolumn") [
                include_content ()
            ],
            
            div (id_="sidebar") [
                include_sidebar ()
            ],

            div (id_="footer") [
                p [ 'Copyright ', E.copy, ' 2011, %(blog_author)s. All rights reserved.' % config]
            ]
        ]
    ]
]
