#!/bin/sh
#
# get access token for default user.
#
curl 'http://localhost:8080/realms/clp/protocol/openid-connect/token'  \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'client_id=clp-client' --data-urlencode 'grant_type=password' --data-urlencode 'username=user' --data-urlencode 'password=user'
