# openkaart-api

## scraper development

* docker pull todorus/openkaart-scraper:dev
* cd into the project root
* docker run -it -v scrapers:/scrapers todorus/openkaart-scraper:dev

You now have a running docker instance with all dependencies installed and a
postgresl database running. The scrapers directory is mounted on the Docker
container so you can make any change using your editor and run the scrapers in
the container by:
'''
/scrapers/run_scrapers.py
'''
