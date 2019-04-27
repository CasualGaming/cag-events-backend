FROM python:3.6

WORKDIR /app

# Application files
COPY requirements requirements/
COPY core core/
COPY apps apps/
COPY manage.py ./
COPY docker-entrypoint.sh ./
COPY uwsgi.ini ./
RUN mkdir -p log

# Extra files
COPY CHANGELOG.md ./
COPY CONTRIBUTORS ./
COPY LICENSE ./
COPY MAINTAINERS ./

# Configure
RUN pip install -r /app/requirements/production.txt

# HTTP
EXPOSE 8000
# WSGI
EXPOSE 8001

CMD ["/bin/bash", "docker-entrypoint.sh"]
