#!/bin/bash

TIMESTAMP=`date +"%Y%m%d%H%M%S"`
source .env
PGPASSWORD=$POSTGRES_PASSOWRD
docker-compose exec db pg_dump funcrowd -U $POSTGRES_USER -W > "./backups/funcrowd-db.$TIMESTAMP.bak.sql"

