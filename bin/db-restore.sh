#!/bin/bash

source .env
docker-compose exec db psql funcrowd -U $POSTGRES_USER -f "/var/lib/backups/$1"

