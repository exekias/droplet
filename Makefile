all:

.PHONY: env

sense: flake8 test

flake8:
	flake8 nazs

test: env
	. env/bin/activate; PYTHONPATH=.         \
    DJANGO_SETTINGS_MODULE=nazs.test_settings \
    fakeroot django-admin.py test

clean:
	rm -rf debian/*.debhelper \
           debian/nazs \
           build/ \
           *.egg-info \
           *.tar.gz \
           *.dsc \
           env

deb:
	dpkg-buildpackage -uc -us

copy-deb:
	cp ../*.deb /nazs

env: env/bin/activate

env/bin/activate: requirements.txt
	test -d env || virtualenv env
	. env/bin/activate; pip install -U -r requirements.txt
	touch env/bin/activate

docker:
	docker build -t nazs-make .

docker-build: docker
	docker run -v $(shell readlink -f .):/nazs nazs-make deb copy-deb

docker-test: docker
	docker run -v $(shell readlink -f .):/nazs nazs-make sense
