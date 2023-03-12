FROM giovtorres/docker-centos7-slurm:latest as base


FROM base as build

# need for download instant client
RUN set -ex \
    && yum makecache fast \
    && yum -y install  \
        curl  \
        unzip \
    && rm -rf /var/cache/yum

# fetch oracle instant client
RUN set -ex \
    && curl \
        "https://download.oracle.com/otn_software/linux/instantclient/213000/instantclient-basiclite-linux.x64-21.3.0.0.0.zip" \
        > /tmp/instantclient-basiclite-linux.x64.zip \
    && unzip /tmp/instantclient-basiclite-linux.x64.zip -d /usr/lib/oracle

RUN echo "NAMES.DIRECTORY_PATH = ( TNSNAMES, LDAP )"          >> /usr/lib/oracle/instantclient_21_3/network/admin/sqlnet.ora \
    && echo "NAMES.DEFAULT_DOMAIN = UFZ.DE"                      >> /usr/lib/oracle/instantclient_21_3/network/admin/sqlnet.ora \
    && echo "NAMES.LDAP_CONN_TIMEOUT = 1"                        >> /usr/lib/oracle/instantclient_21_3/network/admin/sqlnet.ora \
    && echo "DIRECTORY_SERVERS = (tnsnames.intranet.ufz.de:389)" >> /usr/lib/oracle/instantclient_21_3/network/admin/ldap.ora \
    && echo "DEFAULT_ADMIN_CONTEXT = \"ou=oracle,dc=ufz,dc=de\"" >> /usr/lib/oracle/instantclient_21_3/network/admin/ldap.ora \
    && echo "DIRECTORY_SERVER_TYPE = OID"                        >> /usr/lib/oracle/instantclient_21_3/network/admin/ldap.ora

# python requirements
COPY src/tsm-extractor/src/requirements.txt /tmp/requirements_app.txt
COPY src/requirements.txt /tmp/requirements.txt
RUN set -ex \
    && pip3.9 install --upgrade pip \
    && pip3.9 install \
        --no-cache-dir \
        --no-warn-script-location  \
        -r /tmp/requirements_app.txt \
        -r /tmp/requirements.txt


from build as dist


RUN echo /usr/lib/oracle/instantclient_21_3 \
      > /etc/ld.so.conf.d/oracle-instantclient.conf  \
    && ldconfig


# make /work (like in eve) and make it read and writeable
RUN mkdir -p /work/sontsm && chmod -R a+rwx /work

# add user sontsm (same user as we have on EVE)
RUN useradd --uid 1000 -m sontsm
USER sontsm
WORKDIR /home/sontsm
COPY src .

# The entrypoint.sh needs to be run as root, but the
# webserver and invoked comands should be run as `sontsm`
# (our eve user). Actually this is not quite easy, because
# changing the user with `su` either requires a script
# (current case) or a single command (with -c). In the
# latter case all given parameters will be interpreted
# as params for `su`, instead as for the python script.
# Thats the reason we go for the first case and use a
# wrapper script (`pipe.sh`), which replace itself with
# the next following command (`python ...`) and all its
# parameters by using bash magic (`exec "$@"`).
USER root
COPY pipe.sh /pipe.sh

ENTRYPOINT [ \
    "/tini", "--", \
    "/usr/local/bin/docker-entrypoint.sh", \
    "su", "sontsm", "/pipe.sh", "--", \
    "python3.9", "webapi/server.py" \
    ]

CMD ["--mqtt-broker", "None"]
