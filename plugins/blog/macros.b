# load plugin stylesheets	
macro ('include_css', lambda:
    [ [ link (rel="stylesheet", type_="text/css", href="%s" % _css) 
        for _css in plugins.css (_plugin) ] 
      for _plugin in plugins.index (v.current_page) ]
),

# load plugin javascript
macro ('include_js', lambda:
     [ [ script (type_="text/javascript", src="%s" % _js) 
         for _js in plugins.js (_plugin) ]
       for _plugin in plugins.index (v.current_page) ]
),

# include content plugins
macro ('include_content', lambda: 
    [ [ include (_tpl, loader=plugin_loader)
        for _tpl in plugins.templates (_plugin) ]
      for _plugin in plugins.index (v.current_page, 'content') ]
),

# include sidebar plugins
macro ('include_sidebar', lambda:
    [ [ include (_tpl, loader=plugin_loader)
        for _tpl in plugins.templates (_plugin) ]
      for _plugin in plugins.index (v.current_page, 'sidebar') ]
)

