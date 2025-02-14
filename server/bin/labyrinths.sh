#!/bin/sh

#
# Usage:
#   labyrinths.sh user_name password '{"name":"simple"}'
#

curl -v -XGET 'http://localhost:8000/labyrinth/' -H "Authorization: Bearer $(curl -XPOST 'http://localhost:8080/realms/clp/protocol/openid-connect/token' -k -H 'Content-Type: application/x-www-form-urlencoded' -d 'username=philipp&password=philipp&grant_type=password&client_id=clp-client' | jq -r '.access_token')"
