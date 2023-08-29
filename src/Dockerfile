ARG CENTOS_VERSION=7
ARG QUICK_BUILD="false"
ARG PYTHON_VERSION=3.11.5

FROM centos:${CENTOS_VERSION}

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

USER root
WORKDIR /root

RUN yum install -y epel-release && \
    yum install -y wget make gcc openssl openssl-devel bzip2-devel htop tmux libffi-devel sqlite-devel readline-devel ncurses-devel gdbm-devel xz-devel openssl11 openssl11-devel tk-devel uuid-devel && \
    yum groupinstall -y 'Development Tools'

RUN echo "Building Python ${PYTHON_VERSION}"

RUN curl -L -o Python-$PYTHON_VERSION.tgz https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tgz && \
    tar -xzf Python-$PYTHON_VERSION.tgz -C /opt/ && \
    rm Python-$PYTHON_VERSION.tgz && \
    cd /opt/Python-$PYTHON_VERSION/ && \
    export CFLAGS=$(pkg-config --cflags openssl11) && \
    export LDFLAGS=$(pkg-config --libs openssl11) && \
    if [ "${QUICK_BUILD}" = true ] ; then OPTIMIZATION="" ; else OPTIMIZATION="--enable-optimizations --with-lto"; fi && \
    ./configure --with-system-ffi --with-computed-gotos --enable-loadable-sqlite-extensions --enable-shared ${OPTIMIZATION} && \
    nproc="$(nproc)" && \
    make -j "$nproc" && \
    make altinstall && \
    ln -sfn /usr/local/lib/libpython${PYTHON_VERSION%.*}.so.1.0 /usr/lib64/libpython${PYTHON_VERSION%.*}.so.1.0 && \
    ln -sfn /usr/local/bin/python${PYTHON_VERSION%.*} /usr/bin/python3 && \
    ln -sfn /usr/local/bin/python${PYTHON_VERSION%.*}-config /usr/bin/python3-config && \
    ln -sfn /usr/local/bin/pip${PYTHON_VERSION%.*} /usr/bin/pip3 && \
    rm -rf /opt/Python-$PYTHON_VERSION

RUN echo "Python ${PYTHON_VERSION} has been successfully installed and is accessible at /usr/local/bin/python3."

RUN yum install --nogpgcheck -y unzip mysql-devel git vim && \
    yum clean all && \
    yum autoremove -y
