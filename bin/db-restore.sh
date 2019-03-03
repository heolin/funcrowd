#!/bin/bash

source .env
docker-compose exec db pg_restore -Fc --dbname=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:5432/funcrowd "/var/lib/backups/$1"

