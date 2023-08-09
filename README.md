## Delphai challenge

### First task
The first task is about snapshotting a MongoDB cluster using a Python script.
To run the project, you need to have a MongoDB cluster already installed and accessible by the script,
and a Python3.10+.

Executing the projects needs only the following steps:

1- `cd task_1`

2- `make init`

3- `python3.10 main.py "mongodb://localhost:27017/admin?replicaSet=rs0"` 

(Please change the connection parameters according to your usecase.)

> **NOTE:** The project for sure can have other improvements, such as unit testing, e2e testing,
> proper logging with JSON format, metrics, retry mechanisms, etc... But let's stick to basic
> functionalities right now.
