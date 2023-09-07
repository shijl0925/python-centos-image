ARG CENTOS_VERSION as base_image

FROM centos:${CENTOS_VERSION}

RUN yum -y update && yum -y upgrade

RUN yum install -y epel-release && yum install -y wget make gcc openssl openssl11

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

RUN localedef -c -f UTF-8 -i en_US en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

FROM base_image as building_image

ARG QUICK_BUILD
ARG PYTHON_VERSION
# ARG OPENSSL_VERSION="3.1.1"

RUN yum install -y epel-release && \
    yum install -y openssl-devel bzip2-devel libffi-devel \
  sqlite-devel readline-devel ncurses-devel gdbm-devel xz-devel openssl11-devel \
  tk-devel uuid-devel perl nss-devel zlib-devel perl-IPC-Cmd

RUN yum groupinstall -y 'Development Tools'

#RUN echo "Building openssl ${OPENSSL_VERSION}"
#RUN curl -L -o openssl-${OPENSSL_VERSION}.tar.gz https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz && \
#    tar -xzf openssl-${OPENSSL_VERSION}.tar.gz -C /opt/ && \
#    rm openssl-${OPENSSL_VERSION}.tar.gz && \
#    cd /opt/openssl-${OPENSSL_VERSION}/ && \
#    ./config --prefix=/usr/local/openssl-${OPENSSL_VERSION} --openssldir=/usr/local/openssl-${OPENSSL_VERSION} && \
#    make && \
#    make install

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
    rm -rf /opt/Python-$PYTHON_VERSION

# We make sure to remove all the fluff
# recipe taken from the official image https://github.com/docker-library/python/
# RUN find /usr/local -depth \
#   \( \
#   \( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
#   -o \
#   \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
#   \) -exec rm -rf '{}' +;

RUN echo "Python ${PYTHON_VERSION} has been successfully installed and is accessible at /usr/local/bin/python3."

FROM base_image
RUN yum install --nogpgcheck -y --setopt=install_weak_deps=False \
  unzip mysql-devel git vim && \
    yum clean all && \
    yum autoremove -y

COPY --from=building_image /usr/local/ /usr/local/
ARG PYTHON_VERSION
RUN if [ -f "/usr/local/lib/libpython${PYTHON_VERSION%.*}.so.1.0" ] ; then ln -sfn /usr/local/lib/libpython${PYTHON_VERSION%.*}.so.1.0 /usr/lib64/libpython${PYTHON_VERSION%.*}.so.1.0; fi && \
    ln -sfn /usr/local/bin/python${PYTHON_VERSION%.*} /usr/bin/python3 && \
    ln -sfn /usr/local/bin/python${PYTHON_VERSION%.*}-config /usr/bin/python3-config && \
    ln -sfn /usr/local/bin/pip${PYTHON_VERSION%.*} /usr/bin/pip3

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip3 install --upgrade pip

# clean pip cache
RUN python3 -m pip cache purge
