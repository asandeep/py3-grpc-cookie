.PHONY: clean virtualenv test docker

POETRY_DEPENDENCY := "poetry>=0.12"

clean:
	find . -name '*.py[co]' -delete

setup:
	pip install $(POETRY_DEPENDENCY)
	poetry install
	pre-commit install --install-hooks --hook-type pre-commit --hook-type pre-push

virtualenv:
	virtualenv --prompt '|> {{ cookiecutter.project_slug }} <| ' env
	# env/bin/pip install -r requirements-dev.txt
	# env/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo


# PROTOS := $(wildcard *.proto)

# # This
# build: $(PROTOS)

# %:
# 	python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. $<

# # Or This
# build: $(PROTOS)
# 	python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. $^

build:
	cd proto && $(MAKE) build GAPI_COMMON_PROTO_PATH=../$(GAPI_COMMON_PROTO_PATH)

test:
python -m pytest \
	-v \
	--cov={{ cookiecutter.project_slug }} \
	--cov-report=term \
	--cov-report=html:coverage-report \
	tests/

docker: clean
	docker build -t {{ cookiecutter.project_slug }}:latest .

update:
	poetry self:update
	poetry update
	pre-commit autoupdate

makemigrations:
ifeq ($(MSG),)
	@echo "Please provide revision message as MSG=<revision message>"
else
	alembic revision --autogenerate -m "$(MSG)"
endif

migrate:
	alembic upgrade head

# dist: clean
# 	rm -rf dist/*
# 	python setup.py sdist
# 	python setup.py bdist_wheel

# dist-upload:
# 	twine upload dist/*
