#!/bin/bash

TIMESTAMP=`date +"%Y%m%d%H%M%S"`
source .env
docker-compose exec db pg_dump -Fc --dbname=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:5432/funcrowd -f "/var/lib/backups/funcrowd-db.$TIMESTAMP.bak.sql"

