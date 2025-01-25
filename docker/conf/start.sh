#!/bin/sh

/etc/init.d/nginx start
cd /code/
chmod -R 777 .
uwsgi --ini uwsgi.ini