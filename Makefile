all:

sense: pep8 pyflakes test

pep8:
	pep8 nazs

pyflakes:
	pyflakes nazs

test: venv
	. venv/bin/activate; PYTHONPATH=.         \
    DJANGO_SETTINGS_MODULE=nazs.test_settings \
    django-admin.py test

clean:
	rm -rf debian/*.debhelper \
           debian/nazs \
           build/ \
           *.egg-info \
           *.tar.gz \
           *.dsc

deb:
	dpkg-buildpackage -uc -us

copy-deb:
	cp ../*.deb /nazs

venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -U -r requirements.txt
	touch venv/bin/activate

docker-build:
	docker build -t nazs-make .
	docker run -v $(shell readlink -f .):/nazs nazs-make deb copy-deb

docker-test:
	docker build -t nazs-make .
	docker run -v $(shell readlink -f .):/nazs nazs-make test
