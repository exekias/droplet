#!/bin/bash

echo "Creating virtualenv under env dir..."
virtualenv env

echo "Activating virtual env"
. env/bin/activate

echo "Installing pip dependencies"
pip install -r requirements.txt
pip install -r requirements-dev.txt

./manage.py syncdb --migrate --noinput
