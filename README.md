# CaG Events Back-End
Back-end for [CaG Events](https://github.com/CasualGaming/cag-events).

## Requirements

- docker 18.06.0
- docker-compose 1.22.00

## Starting project

### Create env file

    cp fearlessFred/settings/.env.example fearlessFred/settings/.env

### Setup database

    docker-compose run app python /app/manage.py migrate --noinput

    docker-compose run app python /app/manage.py createsuperuser

### Start project


    //If you need to update staticfiles, requirements or nginx.
    docker-compose up -d --build

    //For normal usage, comes with hot reloading
    docker-compose up -d

    //Error output on django engine
    docker-compose logs -f app

    //Shutting down project
    docker-compose down

Project should be now available at [localhost](http://localhost)
