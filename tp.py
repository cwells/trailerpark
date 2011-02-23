#!/usr/bin/python

import logging
from base64 import b64encode

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import breve
breve.Template.namespace = 'v'

define ("config",       default="tp.conf", help="path to config file", type=str)
define ("address",      default="127.0.0.1", help="bind to the given address", type=str)
define ("port",         default=5000, help="run on the given port", type=int)
define ("secret",       default='qc4q24pe4Sadasbvvvsf/wdfc', help="secret for secure cookies", type=str)
define ("couch_host",   default="127.0.0.1", help="URI of couchdb", type=str)
define ("couch_port",   default=5984, help="couchdb port", type=int)
define ("couch_db",     default="tp", help="couchdb database to use", type=str)
define ("couch_design", default="tp", help="couchdb _design document", type=str)
define ("couch_user",   default="", help="couchdb credentials", type=str)
define ("couch_pass",   default="", help="couchdb credentials", type=str)
define ("debug",        default=False, help="restart on code changes", type=bool)
define ("log_blocking", default=0.5, help="log requests that block for n seconds", type=float)
define ("url",          default='http://localhost/', help="blog url", type=str)
define ("title",        default='Trailerpark', help="blog title", type=str)
define ("description",  default='your trash, powered by tornado', help="blog description", type=str)
define ("author",       default='', help="blog author", type=str)
define ("plugins",      default=[], help="an ordered list of plugins to load", type=list)
define ("install",      default=False, help="run installation plugin", type=bool)

tornado.options.parse_config_file (options.config)
tornado.options.parse_command_line ()
options.cookie_secret = b64encode (options.secret)

from handlers.MainHandler import RequestHandler


class Application (tornado.web.Application):
    def __init__ (self):
        handlers = [
            (r"^/",                 RequestHandler), # /
            (r"^/(view|edit)/?",    RequestHandler), # /action, /action/
            (r"^/(view|edit)/(.+)", RequestHandler), # /action/some-article
            (r".*",                 RequestHandler,  {'action': 'view', 'page': '404', 'status': 404})
        ]

        settings = dict (
            cookie_secret=options.cookie_secret,
            login_url="/",
            debug=options.debug
        )

        tornado.web.Application.__init__ (self, handlers, **settings)


def main ():
    http_server = tornado.httpserver.HTTPServer (
        Application (),
        xheaders=True
    )
    http_server.listen (options.port, address=options.address)

    loop = tornado.ioloop.IOLoop.instance ()
    if options.debug:
        loop.set_blocking_log_threshold (options.log_blocking) # issue warning if we block for over 100ms
    try:
        loop.start ()
    except KeyboardInterrupt:
        logging.info ("Exiting due to keyboard interrupt")
        raise SystemExit


if __name__ == "__main__":
    main ()

