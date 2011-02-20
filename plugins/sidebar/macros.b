macro ('sidebar', lambda:
    [ [ include (_tpl, loader=plugin_loader)
        for _tpl in plugins.templates (_plugin) ]
      for _plugin in plugins.index (v.current_page, 'sidebar') ]
)
