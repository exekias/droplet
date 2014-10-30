all:

.PHONY: env

sense: flake8 test

flake8:
	flake8 droplet

test: env
	. env/bin/activate; PYTHONPATH=.         \
    DJANGO_SETTINGS_MODULE=droplet.test_settings \
    fakeroot django-admin.py test

clean:
	rm -rf debian/*.debhelper \
           debian/droplet \
           build/ \
           dist/ \
           *.egg-info \
           *.tar.gz \
           *.dsc \
           env

deb:
	dpkg-buildpackage -uc -us

copy-deb:
	cp ../*.deb /droplet

env: env/bin/activate

env/bin/activate: requirements.txt
	test -d env || virtualenv env
	. env/bin/activate; pip install -U -r requirements.txt
	touch env/bin/activate

docker:
	docker build -t droplet-make .

docker-build: docker
	docker run -v $(shell readlink -f .):/droplet droplet-make deb copy-deb

docker-test: docker
	docker run -v $(shell readlink -f .):/droplet droplet-make sense
