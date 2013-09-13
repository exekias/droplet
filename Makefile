all: env run

env:
	./bootstrap.sh

run:
	./manage.py runserver --nothreading

test:
	./test.py

sense: dockertest pep8

pep8:
	pep8 --exclude=migrations nazs

clean: clean_doc

doc:
	sphinx-apidoc  nazs -o doc
	make -C doc html

clean_doc:
	ls doc/*.rst | grep -v index.rst | xargs -r rm
	rm -rf doc/_*

.PHONY: env doc

# Docker

dockertest:
	docker run -i -t -v $(shell pwd):/nazs exekias/python /bin/bash -c \
           "cd /nazs && ./test.py"
