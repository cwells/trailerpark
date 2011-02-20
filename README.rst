Trailerpark is a blog.

*Status:*

 On the horizon.  Lacks basic features such as creating articles, so don't crack open the Coors Light just yet.


*Requirements:*

 - Python 2.6 or later (3 not supported)
 - CouchDB
 - Tornado_
 - Breve_     
 - Some plugins may have additional dependencies


*Deployment:*

Nginx_ is recommended.  Here's a basic Nginx configuration for Trailerpark::

 server {
     listen      80;
     server_name localhost _;
 
     access_log  /var/log/nginx/trailerpark-access_log;
     error_log   /var/log/nginx/trailerpark-error_log info;
 
     root /var/www/trailerpark/static;
     ssi on;

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



.. _Tornado: https://github.com/facebook/tornado
.. _Breve:   https://github.com/cwells/breve
.. _Nginx:   http://wiki.nginx.org
