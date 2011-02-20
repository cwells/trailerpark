import os, re, imp, logging
import breve
from tornado.options import options
from libs import couch
from libs.couch import BlockingCouch as CouchDB

#
# plugin api, unspecified values assume defaults below
#
api = {
    'depends':   list,            # list of plugins this plugin depends on
    'provides':  str,             # use this name in dependency resolution rather than plugin name
    'target':    lambda: None,    # where plugin is to be rendered
    'url':       lambda: '.*',    # regex of urls plugin is to be rendered on
    'css':       list,            # css resources
    'js':        list,            # javascript resources
    'index':     lambda: 'index', # primary template to render
    'templates': list,            # template resources
    'views':     list,            # couchdb views needed at render time
    'macros':    list,            # macros to be made globally available
    'install':   dict,            # resources to be created during --install. currently: views, docs are supported
}

class Plugins (object):
    ''' singleton that manages plugins.
    Useful methods:
    has (plugin)       - tests if a plugin is available
    grab (plugin)      - tests if a plugin is available, and removes it from index()
    index (target)     - returns list of plugins that match a target
    css (plugin)       - returns css resources for a plugin
    js (plugin)        - returns javascript resources for a plugin
    templates (plugin) - returns template resources for a plugin
    macros (plugin)    - returns global macro definitions for a plugin
    '''
    def __init__ (self):
        logging.info ("=== loading plugins ===")
        self._plugins = {}
        self._skip = []
        for p in options.plugins:
            module = self.load (p)
            if not module:
                continue
            self._plugins [p] = module

        unmet = self.check_dependencies ()
        options.plugins = [p for p in options.plugins 
                           if (p in self._plugins and p not in unmet)]
        if unmet:
            logging.error ("unmet dependencies for plugins: %s" % ', '.join (unmet))
            logging.info ("successfully loaded plugins: %s" % ', '.join (options.plugins))
        else:
            logging.info ("successfully loaded all plugins")

        self.configure_theme ()

    def load (self, plugin):
        '''import and initialize a single plugin
        '''
        logging.info ("loading %s plugin" % plugin)
        try:
            module = imp.load_source (plugin, 'plugins/%s/plugin.py' % plugin)
        except SystemExit, e:
            logging.error ("%s plugin exited: %s" % (plugin, e))
            return
        except:
            logging.error ("failed loading %s plugin" % plugin)
            if options.debug: raise
            return
        
        self.pluginify (module)
        if options.install:
            self.install (plugin, module)

        return module

    def __getitem__ (self, key):
        '''return plugin named by key
        '''
        return self._plugins [key]

    def __contains__ (self, item):
        return item in self._plugins

    def configure_theme (self):
        logging.info ("=== prepare theme ===")
        theme = None
        for p in options.plugins:
            if self._plugins [p].provides == 'theme':
                theme = p
                options.templates = 'plugins/%s' % theme
                options.index = self._plugins [p].index
        if theme:
            logging.info ("using theme: %s" % theme)
        else:
            logging.error ("no theme found")

    def check_dependencies (self):
        '''plugin dependency check.  circular references are removed.
        returns list of unresolved dependencies
        '''
        def depcheck (start, deps, unresolved, circle):
            if start in deps:
                for d in deps [start]:
                    if d in circle:
                        logging.warn ('breaking circular dependency: %s' % d)
                        deps [start].remove (d)
                    if not depcheck (d, deps, unresolved, circle + [d]):
                        if start not in unresolved:
                            unresolved [start] = d
                            logging.error ('%s depends on %s but no plugin provides it' % (start, d))
                        return False
                return True
        
        logging.info ('checking plugin dependencies')

        unresolved = {}
        graph = {}
        for p in self._plugins:
            if self._plugins [p].provides:
                _name = self._plugins [p].provides
            else:
                _name = p
            graph [_name] = self._plugins [p].depends
        for p in graph:
            depcheck (p, graph, unresolved, [p])

        return unresolved
    
    def pluginify (self, module):
        '''ensure plugin represents entire api
        '''
        for k, v in api.items (): 
            if not hasattr (module, k):
                setattr (module, k, v ())

    def install (self, plugin, module):
        '''call each install procedure
        '''
        couchdb = CouchDB (options.couch_db, options.couch_host, options.couch_port)
        for k in module.install:
            logging.info ('%s.install (%s)' % (plugin, k))
            method = "install_%s" % k
            if hasattr (self, method):
                getattr (self, method)(couchdb, module.install [k])

    def install_docs (self, couchdb, docs):
        '''install procedure for couchdb docs
        '''
        for d in docs:
            try:
                existing = couchdb.get_doc (d ['_id'])
            except couch.NotFound:
                existing = {}
            existing.update (d)
            couchdb.save_doc (existing)
            
    def install_views (self, couchdb, vdefs):
        '''install procedure for couchdb views
        '''
        _id = '_design/%s' % options.couch_design
        for v in vdefs:
            try:
                doc = couchdb.get_doc (_id)
            except couch.NotFound:
                doc = {}
            doc ['views'].update (vdefs)
            couchdb.save_doc (doc)

    def index (self, url, target=None):
        '''return a list of plugins for a named target
        '''
        for p in options.plugins: # retain order
            if p in self._skip: 
                continue
            plugin = self._plugins [p]
            if target is None or plugin.target == target:
                if plugin.url is None or re.match (plugin.url, url):
                    yield p

    # public API
    def has (self, plugin):
        '''similar to dict.get() except the 
        default is hard-coded to be an empty string 
        to make it invisible in templates.
        '''
        return self._plugins.get (plugin, '')

    def grab (self, plugin):
        '''tests for a plugin and prevents it from
        being rendered a second time by dropping it
        from the index.
        '''
        p = self._plugins.get (plugin, '')
        if p:
            if p not in self._skip:
                self._skip.append (plugin)
        return p

    def css (self, plugin):
        '''return the css resources for a plugin
        '''
        return [ '/plugins/%s/%s' % (plugin, css) 
                 for css in self._plugins [plugin].css]

    def js (self, plugin):
        '''return the javascript resources for a plugin
        '''
        return [ '/plugins/%s/%s' % (plugin, js) 
                 for js in self._plugins [plugin].js]

    def templates (self, plugin):
        '''return the template resources for a plugin
        '''
        return [ 'plugins/%s/%s' % (plugin, tpl) 
                 for tpl in self._plugins [plugin].templates]

    def macros (self, plugin):
        '''return the macro resources for a plugin
        '''
        return [ 'plugins/%s/%s' % (plugin, macro) 
                 for macro in self._plugins [plugin].macros]


class PluginTemplateLoader (object):
    '''breve loader that uses a path relative to 
    the plugin directory
    '''
    __slots__ = []

    def stat (self, template, root):
        return template, long (os.stat (template).st_mtime)
    
    def load (self, uid):
        return file (uid, 'U').read ()


plugins = Plugins ()
breve.register_global ('plugins', plugins)
breve.register_global ('plugin_loader', PluginTemplateLoader ())
