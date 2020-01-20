FROM fedora:rawhide

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

LABEL summary="Image for running automatic tests of pyreq2rpm in Travis CI" \
      name="pyreq2rpm-tests" \
      maintainer="Gordon Messmer <gordon.messmer@gmail.com>"

RUN INSTALL_PKGS="python3 python3-pytest rpm-build" && \
    dnf -y install --setopt=install_weak_deps=false --setopt=tsflags=nodocs \
                   --setopt=deltarpm=false $INSTALL_PKGS && \
    dnf clean all

CMD ["/usr/bin/python3", "-m", "pytest"]