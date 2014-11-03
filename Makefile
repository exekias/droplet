all:

.PHONY: env

sense: flake8 test report-coverage

flake8: env
	. env/bin/activate; flake8 droplet

test: env
	. env/bin/activate; PYTHONPATH=.         \
    DJANGO_SETTINGS_MODULE=droplet.test_settings \
    fakeroot coverage run --source='droplet' ./env/bin/django-admin.py test

report-coverage:
	coverage report

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
	. env/bin/activate; pip install -U -r requirements-dev.txt
	touch env/bin/activate

docker:
	docker build -t droplet-make .

docker-build: docker
	docker run -v $(shell readlink -f .):/droplet droplet-make deb copy-deb

docker-test: docker
	docker run -v $(shell readlink -f .):/droplet droplet-make sense
