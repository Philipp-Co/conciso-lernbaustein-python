#!/bin/sh
#
# export realm settings and users to file.
#
docker exec -it iam sh -c "/opt/keycloak/bin/kc.sh export --realm clp --file opt/keycloak/data/clp-realm.json"
docker cp iam:/opt/keycloak/bin/clp-realm.json .
