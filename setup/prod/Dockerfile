FROM python:3.7

WORKDIR /app

# Application files
COPY requirements requirements
COPY src src
COPY setup/prod/docker-entrypoint.sh ./
COPY setup/prod/uwsgi.ini ./
RUN mkdir -p log

# Extra files
COPY CHANGELOG.md ./
COPY CONTRIBUTORS ./
COPY LICENSE ./
COPY MAINTAINERS ./

# Configure app
RUN pip3 install -r requirements/production.txt

# HTTP
EXPOSE 8000
# WSGI
EXPOSE 8001

CMD ["/bin/bash", "docker-entrypoint.sh"]
