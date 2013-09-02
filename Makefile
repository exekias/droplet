all: env run

FORCE:

env: FORCE
	./bootstrap.sh

run:
	./manage.py runserver

test: prepare_coverage
	./manage.py test --with-coverage --cover-package=nazs
	@rm .coverage

dockertest: prepare_coverage
	docker run -i -t -v $(shell pwd):/nazs exekias/python /bin/bash -c \
           "cd /nazs && ./manage.py test --with-coverage --cover-package=nazs"
	@rm .coverage

sense: dockertest pep8

pep8:
	pep8 nazs

prepare_coverage:
	@touch .coverage
	@chmod 666 .coverage

