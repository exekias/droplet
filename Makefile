all: env run

FORCE:

env: FORCE
	./bootstrap.sh

run: env
	./manage.py runserver

test: env
	./manage.py test --with-coverage --cover-erase --cover-package=nazs

sense: vagranttest pep8

pep8:
	pep8 nazs


# Vagrant

vagrantup: env
	vagrant up
	vagrant ssh -c "cd /nazs && sudo ./manage.py runserver 0.0.0.0:8000"

vagrantrun: vagrantup

vagranttest: vagrantup
	vagrant ssh -c "cd /nazs && sudo ./manage.py test --with-coverage --cover-erase --cover-package=nazs"


# Docker

dockertest: env
	docker run -i -t -v $(shell pwd):/nazs exekias/python /bin/bash -c \
           "cd /nazs && ./manage.py test --with-coverage --cover-erase --cover-package=nazs"
