# funcrowd


# Setup
1. Run
`docker-compose up app`

# Examples
How to create an example task

1. Run
`docker-compose up notebook`

2. Open
`notebooks/examples/example_task-ratio/1. Create the task.ipynb`

3. Follow the steps in the notebook


## After db restore

After running db restore there may be problem with primary key sequence.
To fix that run following command:
`docker-compose exec app ./manage.py sqlsequencereset <app_name>`

