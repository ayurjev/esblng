#!/bin/bash

python3 migrate.py
uwsgi /uwsgi.ini
