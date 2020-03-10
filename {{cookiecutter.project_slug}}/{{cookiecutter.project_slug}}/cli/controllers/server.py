import time
from concurrent import futures

import cement
import grpc

from {{cookiecutter.project_slug}}.app.py.services import helloworld
from {{cookiecutter.project_slug}}.proto.v1 import helloworld_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class HelloworldServer(cement.Controller):
    class Meta:  # pylint: disable=missing-class-docstring
        label = "server"
        stacked_type = "nested"
        description = "Hello world server."

    def _default(self):
        """Starts server running greeter service."""
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        helloworld_pb2_grpc.add_GreeterServicer_to_server(
            helloworld.GreeterServicer(), server
        )
        server.add_insecure_port("[::]:50051")
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)
