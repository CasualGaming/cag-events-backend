# Development

## Conventions

- All changes to the application must be added to the changelog (`CHANGELOG.md`), excluding changes that update build tools, changes to the code that doesn't affecting the application, etc.
- The code should be linted. If the code is not formatted correctly, CI will fail. Run `manage/lint.sh` to run the linter.
- Don't upgrade deps without making sure that they don't break anything. Read the changelogs. Run `manage/upgrade-deps.sh` to upgrade the deps.

## Code Style

- Add docstrings to all significant classes and functions.
- Double quotes all the way. Single quotes may be used to avoid escaping double quotes within the string. (Single quotes was used here previously.)

## Tools

- Git ([Git CLI](https://git-scm.com) or [GitHub for Windows](https://windows.github.com/))
- Python 3.7 w/ pip
- Docker and Docker Compose (recommended)
- VS Code (optional)
  - flake8 linter extension
- Travis Tool (optional)

### Configure Git
```bash
git config --global core.autocrlf false
git config --global user.name <username>
git config --global user.email <email-address>
```

... or use GitHub for Windows.

### (Optional) Install Travis Tool
Optional, used only for encrypting Travis CI secrets and files and stuff.
```bash
sudo apt install ruby-dev rubygems
sudo gem install travis
```

## Running

### Settings

- **TODO**
- OpenID Connect:
  - At CaG, we use our Keycloak server with realm "dev" with client "cag-events-local" for local testing.

### Scripts

There are scripts to do most stuff. The server can be run either with venv and the Django dev server, within Docker with the Django dev serverm, or within Docker with the uWSGI and nging web servers.

```bash
# Clean-up/delete run stuff like the DB, logs, etc.
manage/clean.sh

# Setup the virtualenv and stuff, required for most scripts below
manage/setup.sh

# Run the dev server in venv
manage/run.sh

# Manually create and activate the venv, for running stuff manually
source manage/activate-venv.sh

# Check dependencies
manage/check-deps.sh

# Upgrade dependencies
manage/upgrade-deps.sh

# Run all checks except for outdated deps (Django validity, unit tests, linter, etc.)
manage/check.sh

# Run tests
manage/test.sh

# Run linter
manage/lint.sh

# Make new migrations (without applying them)
manage/make-migrations.sh
```

### Running in Docker, The Simple Way

- Uses the Django dev server within a Docker container (with hot reloading).
- Uses a SQLite DB back-end.

```bash
# First time or after migration/dependency/etc. changes
manage/docker-simple/setup.sh

# Start the dev server
manage/docker-simple/run.sh

# Run any command in the container (not while already running)
manage/docker-simple/cmd.sh <cmd>

# Run any Django manage command in the container (not while already running)
manage/docker-simple/manage.sh <cmd>
```

### Running in Virtualenv, The Simpler Way

- Uses the Django dev server within a Python virtualenv (with hot reloading).
- Uses a SQLite DB back-end.

```bash
# First time or after migration/dependency/etc. changes
manage/setup.sh

# Start the dev server
manage/run.sh
```

### Running in Docker, The Complete Way

- This way is slow, generally use one of the other ways.
- Uses and nginx proxy.
- Uses a PostgreSQL DB back-end.
- Migrates and collects static on start.
- Most similar to deployment.

```bash
manage/docker-full/setup.sh
manage/docker-full/run.sh
```
