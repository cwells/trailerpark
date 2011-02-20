# include plugin macros
[ [ include (_tpl, loader=plugin_loader)
    for _tpl in plugins.macros (_plugin) ]
  for _plugin in plugins.index (v.current_page) ],

html [
   head [
      title [ config ['blog_title'] ],

      # load plugin stylesheets	
      [ [ link (rel="stylesheet", type_="text/css", href="%s" % _css) 
          for _css in plugins.css (_plugin) ] 
        for _plugin in plugins.index (v.current_page) ],
      
      # load plugin javascript
      [ [ script (type_="text/javascript", src="%s" % _js) 
          for _js in plugins.js (_plugin) ]
        for _plugin in plugins.index (v.current_page) ]      
   ],

   body [
      div (id_="page") [
         div (id_="header") [
            div (id_="headerimg") [
               h1 [ a (href_="/") [ config ['blog_title'] ] ],
               div (class_="description") [ config ['blog_description'] ]
            ]
         ],
         hr,

         # include content plugins
         div (id_="content", class_="narrowcolumn") [
             [ [ include (_tpl, loader=plugin_loader)
                 for _tpl in plugins.templates (_plugin) ]
               for _plugin in plugins.index (v.current_page, 'content') ]
         ],

         div (id_="sidebar") [
            # include sidebar plugins
            [ [ include (_tpl, loader=plugin_loader)
                for _tpl in plugins.templates (_plugin) ]
              for _plugin in plugins.index (v.current_page, 'sidebar') ]
         ],
         hr,

         div (id_="footer") [
            p [ 'Copyright ', E.copy, ' 2011, %(blog_author)s. All rights reserved.' % config]
         ]
      ]
   ]
]
