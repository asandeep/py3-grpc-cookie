import logging
import os

import grpc

from {{cookiecutter.protobuf_namespace}}.proto.{{cookiecutter.project_slug}}.v1 import helloworld_pb2, helloworld_pb2_grpc

LOGGER = logging.getLogger(__name__)


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f"Hello, {request.name}!")
