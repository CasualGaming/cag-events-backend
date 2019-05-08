[![GitHub release](https://img.shields.io/github/release/CasualGaming/cag-events-backend.svg)](https://github.com/CasualGaming/cag-events-backend/releases)
[![Build Status](https://travis-ci.com/CasualGaming/cag-events-backend.svg?branch=master)](https://travis-ci.com/CasualGaming/cag-events-backend)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?branch=master&project=CasualGaming_cag-events-backend&metric=alert_status)](https://sonarcloud.io/dashboard?id=CasualGaming_cag-events-backend)
[![Known Vulnerabilities](https://snyk.io/test/github/CasualGaming/cag-events-backend/badge.svg)](https://snyk.io/test/github/CasualGaming/cag-events-backend)

# CaG Events Back-End
Back-end for [CaG Events](https://github.com/CasualGaming/cag-events).

* [Travis CI](https://travis-ci.com/CasualGaming/cag-events-backend)
* [Docker Hub](https://hub.docker.com/r/casualgaming/cag-events-backend)
* [SonarCloud](https://sonarcloud.io/dashboard?id=CasualGaming_cag-events-backend)

# Tools

- [Git](https://git-scm.com) or [GitHub for Windows](https://windows.github.com/)
- Python 3.7 w/ pip
- Docker and Docker Compose (recommended)
- VS Code (optional)
  - flake8 linter extension
- Travis Tool (optional)

## Configure Git
```bash
git config --global core.autocrlf false
git config --global user.name <username>
git config --global user.email <email-address>
```

... or use GitHub for Windows.

## (Optional) Install Travis Tool
Optional, used for encrypting Travis CI secrets and files and stuff.
```
sudo apt install ruby-dev rubygems
sudo gem install travis
```

## Running

There are scripts to do most stuff. The server can be run either with venv and the Django dev server, within Docker with the Django dev serverm, or within Docker with the uWSGI and nging web servers.

```bash
# Clean-up run stuff
manage/clean.sh

# Setup the virtualenv and stuff (used both for dev stuff and for running in venv)
manage/setup.sh

# Run the dev server in venv
manage/run.sh

# Activate the venv, for running stuff manually (create it if it doesn't exit)
source manage/activate-venv.sh

# Check dependencies
manage/check-deps.sh

# Upgrade dependencies
manage/upgrade-deps.sh

# Run all checks (Django validity, unit tests, linter, etc.)
manage/check.sh

# Run tests
manage/test.sh

# Run linter
manage/lint.sh

# Make new migrations (without applying them)
manage/make-migrations.sh
```

### Running in Docker, The Simple Way

- The recommended way for development.
- Uses the Django dev server within the container (with hot reloading).
- Uses a SQLite DB back-end.
- Has development requirements in addition.

```bash
# First time and after image/requirement/migration/etc changes
manage/docker-simple/setup.sh

# Start the dev server
manage/docker-simple/run.sh

# Run any command in the container (not while already running)
manage/docker-simple/cmd.sh <cmd>

# Run any Django manage command in the container (not while already running)
manage/docker-simple/manage.sh <cmd>
```

### Running in Docker, The Full Way

- The recommended way for testing.
- Uses and nginx proxy.
- Uses a PostgreSQL DB back-end.
- Migrates and collects static on start.
- Most similar to deployment.

```bash
manage/docker-full/setup.sh
manage/docker-full/run.sh
```

## (Dunno what to call this)

- All changes to the application must be added to the changelog (`CHANGELOG.md`), excluding changes that update build tools, changes to the code that doesn't affecting the application, etc.
- Add docstrings to all significant classes and functions.
- The code should be linted. If the code is not formatted correctly, CI will fail. Run `manage/lint.sh` to run the linter.
- Don't upgrade deps without making sure that they don't break anything. Read the changelogs. Run `manage/upgrade-deps.sh` to upgrade the deps.

## Code Style

- Double quotes all the way. Single quotes may be used to avoid escaping double quotes within the string. (Single quotes was used here previously.)
