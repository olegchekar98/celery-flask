# Asynchronous Tasks with Flask and Celery

Example of how to handle background csv reading with Flask, Celery, and Docker.


## Want to use this project?

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Open your browser to [http://localhost:5004](http://localhost:5004).

Upload a new .csv file:

```sh
$ curl http://localhost:5004/files 
```

Check the status and download file in SUCCESS key:

```sh
$ curl http://localhost:5004/files/<FILE_ID>/
```
