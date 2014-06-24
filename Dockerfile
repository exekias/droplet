FROM ubuntu:14.04
MAINTAINER exekias@gmail.com
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update

# Install dh-virtualenv
RUN apt-get install --no-install-recommends -y git-core devscripts equivs ca-certificates
RUN git clone https://github.com/spotify/dh-virtualenv.git
RUN cd dh-virtualenv && git checkout 0.6 && mk-build-deps -irt'apt-get --no-install-recommends -yq'
RUN cd dh-virtualenv && dpkg-buildpackage -uc -us
RUN dpkg -i dh-virtualenv_0.6_all.deb 2>/dev/null ; apt-get --no-install-recommends -y -f install

# Install build depends (add debian dir only for better caching)
ADD debian/control /tmp/control
RUN mk-build-deps -irt'apt-get --no-install-recommends -yq' /tmp/control

RUN apt-get install -y python-flake8

# Build
VOLUME ["/nazs"]
WORKDIR /nazs
ENTRYPOINT ["/usr/bin/make"]
