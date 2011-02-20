import logging
from tornado.options import options
from libs import couch
from libs.couch import BlockingCouch as CouchDB

install = {
    'docs': [
        { '_id': '_design/%s' % options.couch_design, 'views': {} }
    ]
}

def test_installation ():
    couchdb = CouchDB (options.couch_db, options.couch_host, options.couch_port)
    try:
        doc = couchdb.get_doc ('_design/%s' % options.couch_design)
    except couch.NotFound:
        return False
    return True

def do_installation ():
    couchdb = CouchDB (options.couch_db, options.couch_host, options.couch_port)
    try:
        couchdb.create_db ()
    except couch.PreconditionFailed, couch.Conflict:
        logging.warning ('installer: database named %s already exists. Skipping creation.' % options.couch_db)

if options.install:
    do_installation ()
else:
    if not test_installation ():
        raise SystemExit ("use --install to run this plugin.")
    else:
        logging.info ('installer: installation verified')


