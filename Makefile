
all:

sense:
	pep8 nazs
	pyflakes nazs

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
	docker.io build -t build-nazs .
	docker.io run -v $(shell readlink -f .):/nazs build-nazs

