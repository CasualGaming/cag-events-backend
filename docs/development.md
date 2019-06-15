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
- Docker and Docker Compose
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

### Running the Simple Container
This is the intended way to run the dev server and other tools. It consists of a Django dev server inside a Docker container. Scripts in `manage`, except `manage/ci`, `manage/full` and `manage/venv`, are used to interact with the server and other tools. Configs for it are found in `setup/simple` (don't change these) and `.local/simple` (change these instead). We (Casual Gaming) use our Keycloak server with realm "dev" with client "cag-events-local" for local testing.

Setting up and running the dev server:

```bash
# First time only
# If it tells you to fix the config; fix the config and run it again
manage/setup.sh

# For updating installed requirements, re-collect static files and run migrations,
# not needed the first time
manage/update.sh

# Start the dev server
# Press CTRL+C to stop it
manage/run.sh

# Run unit tests and linter
manage/test.sh
manage/lint.sh

# Run a bunch of tests, do this before committing and pushing
manage/check.sh

# Delete all local files like databases, configs, etc.,
# in case you need to start over
manage/clean.sh

# Most scripts in there have comments inside regarding what they do
```

### Running the Full Container
This setup is meant for testing the app in a more realistic scenario.
It contains the app container, a database container (PostgreSQL) and a reverse proxy container (nginx).

```bash
# First time only
# If it tells you to fix the config; fix the config and run it again
manage/full/setup.sh

# No comment needed
manage/full/run.sh
```

### Setting up Virtualenv
Virtualenv is only meant to be used by IDEs for this project.
It'll give the IDE access to the dependencies used (source code and tools).

```bash
# Create venv, install dependencies inside, etc.
manage/venv/setup.sh

# Now tell your IDE to use the venv
```
