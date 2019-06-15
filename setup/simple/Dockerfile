FROM python:3.7

WORKDIR /app

COPY requirements requirements
RUN pip3 install -r requirements/development.txt

EXPOSE 8000

CMD ["/bin/bash", "docker-entrypoint.sh"]
