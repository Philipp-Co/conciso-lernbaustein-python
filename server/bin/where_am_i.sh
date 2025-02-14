#!/bin/sh

#
# Usage:
#
#   where_am_i.sh user_name password Gandalf
#

curl -v -XGET 'http://localhost:8000/labyrinth/navigate/'$3'/' -H "Authorization: Bearer $(curl -XPOST 'http://localhost:8080/realms/clp/protocol/openid-connect/token' -k -H 'Content-Type: application/x-www-form-urlencoded' -d 'username='$1'&password='$2'&grant_type=password&client_id=clp-client' | jq -r '.access_token')"
