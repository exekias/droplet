
run:
	./manage.py runserver

env:
	./bootstrap.sh

test:
	fakeroot ./manage.py test --with-coverage --cover-package=nazs


