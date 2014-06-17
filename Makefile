all:

sense: pep8 pyflakes test

pep8:
	pep8 nazs

pyflakes:
	pyflakes nazs

test:
	PYTHONPATH=. \
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

docker-build:
	cp Dockerfile.build Dockerfile
	docker build -t build-nazs .
	docker run -v $(shell readlink -f .):/nazs build-nazs

docker-test:
	cp Dockerfile.test Dockerfile
	docker build -t test-nazs .
	docker run -v $(shell readlink -f .):/nazs test-nazs

