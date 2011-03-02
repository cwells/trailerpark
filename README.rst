Trailerpark is a blog.

**Status:**

 On the horizon.  Lacks basic features such as creating articles, so don't crack open the Coors Light just yet.


**Requirements:**

 - Python 2.6 or later (3 not supported)
 - CouchDB_
 - Tornado_
 - Breve_     
 - Trombi_
 - Some plugins may have additional dependencies

**Installation**

 - Edit tp.conf.  Make some changes.
 - Run "./tp.py --install", this will create the database, some views and maybe a doc or two.
 - Run "./tp.py"
 - No software installation at this point, just run it from the source directory.
 - Tornado isn't configured to serve static resources, so you'll need to run it behind a webserver (such as Nginx_).

**Deployment:**

Nginx_ is recommended.  Here's a basic Nginx configuration for Trailerpark::

 server {
     listen      80;
     server_name localhost _;
 
     access_log  /var/log/nginx/trailerpark-access_log;
     error_log   /var/log/nginx/trailerpark-error_log info;
 
     root /var/www/trailerpark/static;

     location / {
         try_files $uri @tornado;
     }

     location @tornado {
         include proxy_params;
         proxy_pass http://127.0.0.1:5000;
     }

     location /plugins {
         location ~ \.py[c~]?|\.b~? { return 404; }
         root /var/www/trailerpark;
     }

     location = /favicon.ico { return 404; }
 }


.. _CouchDB: http://couchdb.apache.org
.. _Tornado: https://github.com/facebook/tornado
.. _Breve:   https://github.com/cwells/breve
.. _Trombi:  https://github.com/inoi/trombi
.. _Nginx:   http://wiki.nginx.org
