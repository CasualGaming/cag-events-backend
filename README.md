# CaG Events Back-End
Back-end for [CaG Events](https://github.com/CasualGaming/cag-events).

## Requirements

- Python 3 w/ pip
- Docker
- Docker Compose
- ++

## Running

There are 4 methods to run the local server. All of them should support both Linux, MacOS and Windows (w/ BASH and stuff).

### Method 1: Manually (OUTDATED) (Not Recommended)

- **OUTDATED** Not recommended.

#### Create env file

    cp core/settings/.env.example core/settings/.env

#### Setup database

    docker-compose run app python /app/manage.py migrate --noinput

    docker-compose run app python /app/manage.py createsuperuser

#### Start project


    //If you need to update staticfiles, requirements or nginx.
    docker-compose up -d --build

    //For normal usage, comes with hot reloading
    docker-compose up -d

    //Error output on django engine
    docker-compose logs -f app

    //Shutting down project
    docker-compose down

Project should be now available at [localhost](http://localhost)

### Method 2: Using Virtualenv

- Better than manual.
- Uses the Django dev server (hot reloading).
- Uses a SQLite DB back-end.
- Migrates and collects static on setup.

```bash
manage/setup-venv.sh
manage/run-venv.sh
```

### Method 3: Using Docker Compose, The Simple Way

- The recommended way for development.
- Uses the Django dev server (hot reloading).
- Uses a SQLite DB back-end.
- Migrates on start.
- Has development requirements in addition.

```bash
manage/setup-docker-simple.sh
manage/run-docker-simple.sh
```

### Method 4: Using Docker Compose, The Full Way

- The recommended way for testing.
- Uses and nginx proxy.
- Uses a PostgreSQL DB back-end.
- Migrates and collects static on start.
- Most similar to deployment.
- All the bells and whistles.

```bash
manage/setup-docker-full.sh
manage/run-docker-full.sh
```
