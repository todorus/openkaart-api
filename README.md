Openkaart Service
==========================
The source the Openkaart project. This service is a webservice that exposes the openkaart api.

Requirements
------------
* Docker

And that's it. Docker will get any additional requirements and setup your development or testing environment.

Development
-----------
You can run the develop script to get you started. The script will build a Docker container and run it.
```
./develop.sh
```
This will start a webserver and echo the hostname and port to the console. It will run app/start_server.py and do a hot reload on code changes within the /app folder. The exception is start_server.py: if you change this file you will need to restart the development environment.

Testing
-------
There is also a script to run the tests.
```
./test.sh
```
Will rebuild all the docker images to make sure everything is up to the latest production configs. In addition it will also build and launch a test container which will run integration tests.

The test container will manipulate the state of the database, by directly connecting to it and wipe/insert data as necessary for the test. Next it will sending http requests to the webserver and check the responses.

Deployment
----------
You will need to adjust the names of the images to match your dockerhub username. You can find these names in:
```
deployment/production.yaml
deployment/server-files/certbot.yaml
deployment/server-files/production.yaml
```
You'll also need to update the server_name directives in the nginx config.
```
deployment/nginx.api.conf
```
Login to your dockerhub account with the docker client. Next run the build script to build the docker images and push them to your repo.
```
./build.sh
```
And for the actual deployment, copy the files in deployment/server-files to your server and run:
```
./init.sh
```
This will run certbot for the first time to acquire/update ssl certificates for your domain. Next run:
```
./deploy.sh
```
To start the application.

#TODO certbot certificate renewal
