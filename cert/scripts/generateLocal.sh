#!/bin/sh

# Сгенерировать локальный https-сертификат для тестов
# http://sial.org/howto/openssl/self-signed/

# Вариант с CA: http://sial.org/howto/openssl/ca/

openssl genrsa 1024 -config openssl.cnf > ../server.key
openssl req -new -x509 -nodes -sha1 -days 365 -key ../server.key -config openssl.cnf > ../server.cert

