all: env run

env:
	./bootstrap.sh

run: env
	./manage.py runserver

test: env
	./test.py

sense: vagranttest pep8

pep8:
	pep8 nazs


# Vagrant

vagrantup: env
	vagrant up

vagrantrun: vagrantup
	vagrant ssh -c "cd /nazs && sudo ./manage.py runserver 0.0.0.0:8000"

vagranttest: vagrantup
	vagrant ssh -c "cd /nazs && sudo ./test.py"


# Docker

dockertest: env
	docker run -i -t -v $(shell pwd):/nazs exekias/python /bin/bash -c \
           "cd /nazs && ./test.py"
