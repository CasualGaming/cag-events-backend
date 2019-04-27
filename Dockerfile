FROM python:3.6-slim

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements requirements/
COPY core core/
COPY apps apps/
COPY manage.py .

RUN pip install -r /app/requirements/all.txt
RUN python manage.py collectstatic --settings=core.settings.local --noinput
RUN rm -rf /app/requirements

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
