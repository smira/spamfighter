#!/bin/sh

# Сгенерировать локальный https-сертификат для тестов
# http://sial.org/howto/openssl/self-signed/

# Вариант с CA: http://sial.org/howto/openssl/ca/

DESTDIR=${1:-..}
BASEDIR=`dirname "$0"`

openssl genrsa 1024 -config "$BASEDIR/openssl.cnf" > "$DESTDIR/server.key"
openssl req -new -x509 -nodes -sha1 -days 365 -key "$DESTDIR/server.key" -config "$BASEDIR/openssl.cnf" > "$DESTDIR/server.cert"

