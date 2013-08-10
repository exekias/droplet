PWD = $(shell pwd)

run:
	./manage.py runserver

env:
	./bootstrap.sh

test:
	./manage.py test --with-coverage --cover-package=nazs

docker_test:
	docker run -i -t -v ${PWD}:/nazs cperez/python /bin/bash -c "cd /nazs && ./manage.py test --cover-package=nazs"

