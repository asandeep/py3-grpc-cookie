#### Cookiecutter Python3 GRPC server

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template to generate Python3 GRPC service.

### Features
* ORM - SQLAlchemy
* Alembic for DB migrations
* Sample GRPC Helloworld server and client implementations
* Dynaconf for configuration management
* Command line interface via cement framework
* Implements a simple helloworld client/server from: https://grpc.io/docs/quickstart/python/

## Getting Started

### Generate Project

```bash
cookiecutter https://github.com/asandeep/py3-grpc-cookie
```

### Setup

```
make setup
```

### Run helloworld application

```
make protobuf
```

```
make run-server
make run-client
```

### Manually execute pre-commit hooks
```
pre-commit run --all-files
```


### Install pre-commit hooks
This will initialize current folder as git repo.

To install pre-commit hooks, make sure that repository is initialized as a GIT repository.

Make sure to select `install_precommit_hooks` during project setup.


### Running tests
```
make test
```

### Generate Docker image
```
make docker
```

### Running helloworld server inside docker
```
make run-docker-server
```

### Deploying app to production

#### Vault Integration
