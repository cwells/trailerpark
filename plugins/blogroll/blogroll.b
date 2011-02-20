div ( class_="box" ) [
    h2 [ "Blogroll" ],
    ul [
        [ li [ a (href=_url) [ span [ img (src='%s/favicon.ico' % _url, style='width:20px; height:20px;'), _title ] ] ]
          for (_url, _title) in [
                ('http://www.omgubuntu.co.uk', 'OMG! Ubuntu'),
                ('http://arstechnica.com', 'ARS Technica'),
                ('http://www.tornadoweb.org', 'Tornado')]
        ]
    ]
]

