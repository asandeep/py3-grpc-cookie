### Setup

```
make setup
```

### Run {{ cookiecutter.project_slug }} application

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


### Running tests
```
make test
```

### Generate Docker image
```
make docker
```

### Running {{ cookiecutter.project_slug }} server in docker
```
make run-docker-server
```

### Deploying app to production

#### Vault Integration
