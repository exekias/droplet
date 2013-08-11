all: env run

FORCE:

env: FORCE
	./bootstrap.sh

run:
	./manage.py runserver

test: coverage
	./manage.py test --with-coverage --cover-package=nazs
	@rm .coverage

docker_test: coverage
	@docker run -i -t -v $(shell pwd):/nazs exekias/python /bin/bash -c \
           "cd /nazs && ./manage.py test --with-coverage --cover-package=nazs"
	@rm .coverage

coverage:
	@touch .coverage
	@chmod 666 .coverage

