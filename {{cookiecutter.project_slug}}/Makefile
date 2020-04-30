.PHONY: clean virtualenv test docker

POETRY_VERSION := "1.0.3"
PROTO_FILES := $(shell find {{ cookiecutter.project_slug }}/ -name "*.proto")
CURRENT_APP_VERSION := $(lastword $(shell poetry version))

clean:
	-find . -name '*.py[ico]' -delete
	-find {{ cookiecutter.project_slug }}/proto \( -name '*.py' ! -name '__init__.py' \) -delete
	-rm -rf dist/*


setup:
	pip install poetry==$(POETRY_VERSION)
	poetry install
	{% if cookiecutter.install_precommit_hooks == "y" %}
	git init
	pre-commit install --install-hooks --hook-type pre-commit --hook-type pre-push
	{% endif %}


docker: clean protobuf
	docker build -t {{ cookiecutter.project_slug }}:latest .
	docker tag {{ cookiecutter.project_slug }}:latest {{ cookiecutter.project_slug }}:$(CURRENT_APP_VERSION)


run-docker-server: docker
	docker run -p 50051:50051 {{ cookiecutter.project_slug }}:latest


run-server: protobuf
	{{ cookiecutter.project_slug }} server


run-client: protobuf
	@echo ""
	@{{ cookiecutter.project_slug }} client hello --from "$(FROM)"


protobuf:
	python -m grpc_tools.protoc -I . \
	--python_out=. --grpc_python_out=. --mypy_out=. $(PROTO_FILES)


proto-docs:
	docker run \
	--rm -v $(CURDIR)/docs:/out \
	-v $(CURDIR)/{{ cookiecutter.project_slug }}/proto:/{{ cookiecutter.project_slug }}/proto \
	pseudomuto/protoc-gen-doc -I . $(PROTO_FILES)

	# Open generated file with default application
	xdg-open docs/index.html


dist: protobuf clean
	poetry build
# dist-upload:
# 	twine upload dist/*


test: protobuf
	-python -m pytest \
		-v \
		--cov={{ cookiecutter.project_slug }} \
		--cov-report=term \
		--cov-report=html:coverage-report \
		--cov-fail-under=80 \
		.

	xdg-open coverage-report/index.html

update:
	poetry update
	{% if cookiecutter.install_precommit_hooks == "y" %}
	pre-commit autoupdate
	{% endif %}


makemigrations:
ifeq ($(MSG),)
	@echo "Please provide revision message as MSG=<revision message>"
else
	alembic revision --autogenerate -m "$(MSG)"
endif


migrate:
	alembic upgrade head
