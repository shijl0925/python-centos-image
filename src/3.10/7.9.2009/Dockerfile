ARG CENTOS_VERSION

FROM centos:${CENTOS_VERSION}

ARG QUICK_BUILD
ARG PYTHON_VERSION

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

RUN localedef -c -f UTF-8 -i en_US en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

USER root
WORKDIR /root

RUN yum -y update && yum -y upgrade

RUN yum groupinstall -y 'Development Tools'

RUN yum install -y epel-release && \
    yum install -y wget openssl openssl-devel bzip2-devel htop tmux libffi-devel \
  sqlite-devel readline-devel ncurses-devel gdbm-devel xz-devel openssl11 openssl11-devel \
  tk-devel uuid-devel

RUN echo "Building Python ${PYTHON_VERSION}"
RUN curl -L -o Python-${PYTHON_VERSION}.tgz https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-${PYTHON_VERSION}.tgz && \
    tar -xzf Python-${PYTHON_VERSION}.tgz -C /opt/ && \
    rm Python-${PYTHON_VERSION}.tgz && \
    cd /opt/Python-${PYTHON_VERSION}/ && \
    export CFLAGS=$(pkg-config --cflags openssl11) && \
    export LDFLAGS=$(pkg-config --libs openssl11) && \
    ./configure --with-system-ffi --enable-loadable-sqlite-extensions --enable-shared --enable-optimizations --with-lto && \
    make && \
    if [ ! "${QUICK_BUILD}" = true ] ; then make test; fi && \
    make altinstall && \
    if [ -f "/usr/local/lib/libpython${PYTHON_VERSION%.*}.so.1.0" ] ; then ln -sfn /usr/local/lib/libpython${PYTHON_VERSION%.*}.so.1.0 /usr/lib64/libpython${PYTHON_VERSION%.*}.so.1.0; fi && \
    ln -sfn /usr/local/bin/python${PYTHON_VERSION%.*} /usr/bin/python3 && \
    ln -sfn /usr/local/bin/python${PYTHON_VERSION%.*}-config /usr/bin/python3-config && \
    ln -sfn /usr/local/bin/pip${PYTHON_VERSION%.*} /usr/bin/pip3 && \
    rm -rf /opt/Python-$PYTHON_VERSION

RUN echo "Python ${PYTHON_VERSION} has been successfully installed and is accessible at /usr/local/bin/python3."

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip3 install --upgrade pip

# clean pip cache
RUN python3 -m pip cache purge

RUN yum install --nogpgcheck -y unzip git vim && \
    yum clean all && \
    yum autoremove -y
