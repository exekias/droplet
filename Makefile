all: env run

FORCE:

env: FORCE
	./bootstrap.sh

run:
	./manage.py runserver

test: prepare_coverage
	./manage.py test --nologcapture --with-coverage --cover-package=nazs
	@rm .coverage

sense: vagranttest pep8

pep8:
	pep8 nazs


# Vagrant

vagrantup:
	vagrant up

vagranttest: vagrantup
	vagrant ssh -c "cd /nazs && sudo ./manage.py test --with-coverage --cover-package=nazs"
	@rm .coverage


# Docker

dockertest: prepare_coverage
	docker run -i -t -v $(shell pwd):/nazs exekias/python /bin/bash -c \
           "cd /nazs && ./manage.py test --with-coverage --cover-package=nazs"

prepare_coverage:
	@touch .coverage
	@chmod 666 .coverage
