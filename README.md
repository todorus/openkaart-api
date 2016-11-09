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
This will start a webserver and echo the hostname and port to the console. It will run any code contained within the "/app" directory.

Any changes inside the "app" directory will be reflected in the webserver.

Testing
-------
There is also a script to run the tests.
```
./test.sh
```
Will rebuild all the docker images to make sure everything is up to the latest production configs. In addition it will also build and launch a test container which will run integration tests by sending http requests to the webserver.

Deployment
----------
*TODO*
