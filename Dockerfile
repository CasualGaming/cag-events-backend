FROM python:3.6-slim

MAINTAINER Mathias Flått

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements/ /app/requirements/
COPY ./apps/  /app/apps/
COPY fearlessFred  /app/fearlessFred/
COPY ./manage.py  /app/

RUN pip install -r /app/requirements/local.txt && python manage.py collectstatic --settings=fearlessFred.settings.local --noinput
RUN rm -rf /app/requirements


EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
