.PHONY: clean virtualenv test docker

POETRY_DEPENDENCY := "poetry>=0.12"

clean:
	find . -name '*.py[co]' -delete

setup:
	pip install $(POETRY_DEPENDENCY)
	poetry install

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
ifeq ($(GAPI_COMMON_PROTO_PATH),)
	@echo "Please provide Google API common proto path as GAPI_COMMON_PROTO_PATH=<absolute/relative path>"
else
	python -m grpc_tools.protoc \
	-I $(GAPI_COMMON_PROTO_PATH) -I . \
	--python_out=. --grpc_python_out=. --mypy_out=. \
	./sentieo/proto/{{ cookiecutter.project_slug }}/v1/convert.proto ./sentieo/proto/{{ cookiecutter.project_slug }}/type/file.proto
endif

update:
	poetry self:update
	poetry update

# dist: clean
# 	rm -rf dist/*
# 	python setup.py sdist
# 	python setup.py bdist_wheel
