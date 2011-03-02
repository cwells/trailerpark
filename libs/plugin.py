import os, re, imp, logging
from functools import partial
import breve
import trombi
from tornado.options import options
from tornado.ioloop import PeriodicCallback
from libs.util import with_ioloop

#
# plugin api, unspecified values assume defaults below
#
api = {
    'depends':   list,            # list of plugins this plugin depends on
    'provides':  str,             # use this name in dependency resolution rather than plugin name
    'url':       lambda: '.*',    # regex of urls plugin is to be rendered on
    'action':    lambda: '.*',    # regex of actions to render on (e.g. edit/article, view/comment)
    'css':       list,            # css resources
    'js':        list,            # javascript resources
    'templates': list,            # template resources
    'views':     list,            # couchdb views needed at render time
    'macros':    list,            # macros to be made globally available
    'install':   dict,            # resources to be created during --install. currently: views, docs are supported
    'index':     lambda: 'index', # primary template to render (for themes only)
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
    @with_ioloop
    def __init__ (ioloop, self):
        logging.info ("=== loading plugins ===")
        self._plugins = {}
        self.couchdb = None

        def callback (db):
            self.couchdb = db

            for p, target in options.plugins:
                module = self.load (db, p, target)
                if module:
                    self._plugins [p] = module

            unmet = self.check_dependencies ()
            options.plugins = [(p, t) for (p, t) in options.plugins 
                               if (p in self._plugins and p not in unmet)]
            if unmet:
                logging.error ("unmet dependencies for plugins: %s" % ', '.join (unmet))
                logging.info ("successfully loaded plugins: %s" % ', '.join (options.plugins))
            else:
                logging.info ("successfully loaded all plugins")

            self.configure_theme ()

            if options.install:
                def shutdown ():
                    if ioloop._events or ioloop._callbacks:
                        return
                    ioloop.stop ()
                    if options.install:
                        logging.info ('Install completed!  Now restart without --install flag.')
                        raise SystemExit

                PeriodicCallback (shutdown, 1000, ioloop).start ()
            else:
                ioloop.stop ()
                logging.info ('Trailerpark is ready.')

        server = trombi.Server ('http://%s:%s' % (options.couch_host, options.couch_port))
        server.get (options.couch_db, callback, create=True)

    def load (self, db, plugin, target=None): 
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
        module.target = target
        if options.install:
            self.install (db, plugin, module)
                
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
        for p in self._plugins:
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

    def install (self, db, plugin, module):
        '''call each install procedure
        '''
        for k in module.install:
            logging.info ('%s.install (%s)' % (plugin, k))
            method = "install_%s" % k
            if hasattr (self, method):
                getattr (self, method)(db, module.install [k])
            else:
                logging.error ('Unknown install method in %s: %s' % (plugin, method))

    def install_docs (self, db, docs):
        '''install procedure for couchdb docs
        '''
        def get_cb (data, doc):
            if not doc or doc.error: # create new doc
                db.set (data, partial (set_cb, data))
            else: # update existing doc
                for k, v in data.items ():
                    try:
                        doc [k] = v 
                    except KeyError: # can't update keys starting with underscore
                        continue
                db.set (data ['_id'], doc, partial (set_cb, data))
        
        def set_cb (data, doc):
            if doc.error:
                logging.warn ("Can't create doc: %s" % doc.msg)

        for d in docs:
            _id = d ['_id']
            db.get (_id, partial (get_cb, d))
            
    def install_views (self, db, views):
        '''install procedure for couchdb views
        '''
        _id = '_design/%s' % options.couch_design

        def get_cb (vdefs, view):
            if view is None or view.error: # create new view
                db.set (_id, {'views': vdefs}, set_cb)
            else: # update existing view
                for k, v in vdefs.items ():
                    try:
                        view [k] = v
                    except KeyError:
                        continue
                db.set (_id, view, set_cb)

        def set_cb (view):
            if view.error:
                logging.warn ("Can't create view: %s" % view.msg)

        vdefs = {}
        for v in views:
            vdefs [v] = views [v]

        db.get (_id, partial (get_cb, vdefs))

    def index (self, pageinfo, target=None):
        '''return a list of plugins for a named target
        '''
        for p, t in options.plugins: # retain order
            plugin = self._plugins [p]
            if target is None or plugin.target == target:
                if re.match (plugin.url, pageinfo ['doc']):
                    if re.match (plugin.action, pageinfo ['action']):
                        yield p

    # public API
    def has (self, plugin):
        '''check if a plugin is provided
        '''
        for p, m in self._plugins.items ():
            if plugin in (p, m.provides):
                return m
        return ''

    def dir (self, plugin, path=''):
        '''return the path of the active plugin
        '''
        return '/plugins/%s/%s' % (plugin, path)

    def css (self, plugin):
        '''return the css resources for a plugin
        '''
        return ['/plugins/%s/%s' % (plugin, css) 
                for css in self._plugins [plugin].css]

    def js (self, plugin):
        '''return the javascript resources for a plugin
        '''
        return ['/plugins/%s/%s' % (plugin, js) 
                for js in self._plugins [plugin].js]

    def templates (self, plugin):
        '''return the template resources for a plugin
        '''
        return ['plugins/%s/%s' % (plugin, tpl) 
                for tpl in self._plugins [plugin].templates]

    def macros (self, plugin):
        '''return the macro resources for a plugin
        '''
        return ['plugins/%s/%s' % (plugin, macro) 
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



