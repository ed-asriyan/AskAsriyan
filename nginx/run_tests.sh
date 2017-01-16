#!/bin/bash

rm -rf reports
mkdir reports

ab -c 10 -n 10000 http://localhost:8001/ > reports/gunicorn_wsgi.txt
ab -c 10 -n 10000 http://localhost:81/ > reports/nginx_gunicorn_wsgi.txt
ab -c 10 -n 10000 http://localhost/static/css/bootstrap.css > reports/nginx_static.txt

