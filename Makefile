all: env run

env:
	./bootstrap.sh

run:
	./manage.py runserver --nothreading --insecure 0.0.0.0:8000

test:
	./test.py

sense: pep8 pyflakes test

pep8:
	pep8 --exclude=urls.py,migrations nazs

pyflakes:
	pyflakes nazs

clean: clean_doc

doc:
	sphinx-apidoc  nazs -o doc
	make -C doc html

clean_doc:
	ls doc/*.rst | grep -v index.rst | xargs -r rm
	rm -rf doc/_*

.PHONY: env doc
