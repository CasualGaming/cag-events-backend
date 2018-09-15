# Requirements

- docker 18.06.0
- docker-compose 1.22.00

# Starting project

## Setup database

    docker-compose run app python /app/manage.py migrate --noinput

---

    docker-compose run app python /app/manage.py createsuperuser

## Start project

    docker-compose up -d --build

Project should be now available at [localhost](http://localhost)