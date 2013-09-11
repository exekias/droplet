all: env run

env:
	./bootstrap.sh

run: env
	./manage.py runserver --nothreading

test: env
	./test.py

sense: dockertest pep8

pep8:
	pep8 --exclude=migrations nazs

# Docker

dockertest: env
	docker run -i -t -v $(shell pwd):/nazs exekias/python /bin/bash -c \
           "cd /nazs && ./test.py"
