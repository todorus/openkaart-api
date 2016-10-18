Openkaart Regions Resource
==========================
The source for a microservice in the Openkaart project. This service is a webservice that exposes the Regions resource.

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
This will start a webserver and echo the hostname and port to the console. It will run any code contained within the "/code" directory.

Any changes inside the "code" directory will be reflected in the webserver.

_This is almost entirely true. The docker does move some stuff around, but if you look at the package names in the current code you should be alright._

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
