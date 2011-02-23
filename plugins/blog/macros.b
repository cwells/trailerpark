# load plugin stylesheets	
macro ('include_css', lambda:
    [ [ link (rel="stylesheet", type_="text/css", href="%s" % _css) 
        for _css in plugins.css (_plugin) ] 
      for _plugin in plugins.index (v._pageinfo) ]
),

# load plugin javascript
macro ('include_js', lambda:
     [ [ script (type_="text/javascript", src="%s" % _js) 
         for _js in plugins.js (_plugin) ]
       for _plugin in plugins.index (v._pageinfo) ]
),

# include content plugins
#   wrapper must be a tag *factory*, that is you cannot pass just 
#       wrapper=div(class_='foo')
#   rather you must pass 
#       wrapper=lambda: div(class_="foo")
#   although you *can* simply pass 
#       wrapper=div
#   since each call to "div" will yield a new div object.
macro ('include_plugins', lambda target, wrapper=invisible:
    [ [ wrapper () [ include (_tpl, loader=plugin_loader) ]
        for _tpl in plugins.templates (_plugin) ]
      for _plugin in plugins.index (v._pageinfo, target) ]
)


