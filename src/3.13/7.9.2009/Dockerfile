ARG CENTOS_VERSION

FROM centos:${CENTOS_VERSION} as base_image
RUN yum -y update && yum -y upgrade

FROM base_image as building_image

ARG QUICK_BUILD
ARG PYTHON_VERSION

RUN yum groupinstall -y 'Development Tools'
RUN yum install -y epel-release && \
  yum install -y bzip2-devel \
  libffi-devel \
  ncurses-devel \
  nss-devel \
  perl \
  perl-IPC-Cmd \
  sqlite-devel \
  wget \
  zlib-devel \
  openssl11-devel

ARG OPENSSL_VERSION="3.2.1"
RUN echo "Building openssl ${OPENSSL_VERSION}"
RUN curl -L -o openssl-${OPENSSL_VERSION}.tar.gz https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz && \
    tar -xzf openssl-${OPENSSL_VERSION}.tar.gz -C /opt/ && \
    rm openssl-${OPENSSL_VERSION}.tar.gz && \
    cd /opt/openssl-${OPENSSL_VERSION}/ && \
    ./config -Wl,-rpath=/usr/local/openssl-${OPENSSL_VERSION}/lib64:/usr/local/lib -Wl,--enable-new-dtags --prefix=/usr/local/openssl-${OPENSSL_VERSION} --openssldir=/usr/local/openssl-${OPENSSL_VERSION} && \
    make && \
    make install

# Make sure the env variable are correctly set for Python to be able
# to link and compile against openSSL.
ENV LDFLAGS "-L/usr/local/openssl-${OPENSSL_VERSION}/lib64/ -Wl,-rpath=/usr/local/openssl-${OPENSSL_VERSION}/lib64:/usr/local/lib"
ENV LD_LIBRARY_PATH "/usr/local/openssl-${OPENSSL_VERSION}/lib/:/usr/local/openssl-${OPENSSL_VERSION}/lib64/"
ENV CPPFLAGS "-I/usr/local/openssl-${OPENSSL_VERSION}/include -I/usr/local/openssl-${OPENSSL_VERSION}/include/openssl"

RUN echo "Building Python ${PYTHON_VERSION}"
RUN curl -L -o Python-${PYTHON_VERSION}.tgz https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-${PYTHON_VERSION}.tgz && \
    tar -xzf Python-${PYTHON_VERSION}.tgz -C /opt/ && \
    rm Python-${PYTHON_VERSION}.tgz && \
    cd /opt/Python-${PYTHON_VERSION}/ && \
    ./configure --with-system-ffi --with-openssl=/usr/local/openssl-${OPENSSL_VERSION} --with-openssl-rpath=auto --enable-loadable-sqlite-extensions --enable-shared && \
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
RUN yum install -y epel-release && yum install --nogpgcheck -y --setopt=install_weak_deps=False \
  openssl11 \
  bzip2 \
  ca-certificates \
  libffi \
  ncurses \
  nss \
  sqlite \
  wget \
  zlib && \
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
