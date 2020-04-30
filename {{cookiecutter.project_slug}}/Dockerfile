FROM python:3.6-slim

LABEL maintainer="{{ cookiecutter.full_name }} <{{ cookiecutter.email }}>"

ARG poetry_version=1.0.3

# Environment varialbes to control python and pip behaviour.
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Application specific variables.
ENV GRPC_SERVICE_PORT="50051" \
    # Specify the environment where this container is deployed. For list of
    # available environments, refer config/settings.toml.
    ENV_FOR_DYNACONF="DEVELOPMENT" \
    DEBUG_LEVEL_FOR_DYNACONF="DEBUG" \
    VAULT_ENABLED_FOR_DYNACONF=false

RUN pip install poetry==${poetry_version}

WORKDIR /{{ cookiecutter.project_slug }}

COPY poetry.lock pyproject.toml /{{ cookiecutter.project_slug }}/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root --no-interaction --no-ansi \
    # TODO(asandeep): Fix logging config so that creting logs directory is not
    # required.
    && mkdir logs

COPY . /{{ cookiecutter.project_slug }}/

CMD ["python", "-m", "{{ cookiecutter.project_slug }}.cli.main", "server"]

EXPOSE ${GRPC_SERVICE_PORT}
