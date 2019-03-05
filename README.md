# funcrowd

## After db restore
After running db restore there may be problem with primary key sequence.
To fix that run following command:
`docker-compose exec app ./manage.py sqlsequencereset <app_name>`

