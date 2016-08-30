# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER todorus

# Update the sources list
RUN apt-get update

RUN apt-get install -y git
RUN useradd -m scraper

# Get the code
USER scraper
WORKDIR /home/scraper
RUN git clone -b feature/scraper https://github.com/todorus/openkaart-api.git
RUN mkdir -p /Volumes/openkaart_data/

# Install Postgres and PostGis
USER root
RUN apt-get install -y postgresql-9.5 postgresql-contrib-9.5
RUN apt-get install -y postgis-2.2
RUN sed -i 's/peer/trust/g' /etc/postgresql/9.5/main/pg_hba.conf

# Configure database
USER postgres
RUN service postgresql start && \
    psql -f openkaart-api/create_database.sql && \
    service postgresql stop

# Install Python and Basic Python Tools
USER root
RUN apt-get install -y python python-dev python-distribute python-pip libpq-dev
RUN pip install -r openkaart-api/scrapers/requirements.txt

# create the database tables
RUN service postgresql start && \
    psql -U postgres -d openkaart_development -c "CREATE EXTENSION postgis;" && \
    python openkaart-api/scrapers/create_database_tables.py  && \
    service postgresql stop

# make sure postgres is running and start the scraper
WORKDIR /home/scraper/openkaart-api/scrapers
CMD service postgresql start && \
    git pull && \
    python run_scrapers.py
VOLUME /volumes/openkaart-data/
