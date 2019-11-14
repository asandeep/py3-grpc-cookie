import time
from concurrent import futures

import grpc
from cement import Controller
from cement.utils.version import get_version_banner

from {{cookiecutter.project_slug}}.app.py.services import helloworld
from {{cookiecutter.protobuf_namespace}}.proto.{{cookiecutter.project_slug}}.v1 import helloworld_pb2_grpc


class HelloworldServer(Controller):
    class Meta:  # pylint: disable=missing-class-docstring
        label = "server"

        # text displayed at the top of --help output
        description = "{{ cookiecutter.project_short_description}}"

    def _default(self):
        """Starts server running greeter service."""
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        convert_pb2_grpc.add_FileConversionServicer_to_server(
            helloworld.GreeterServicer(), server
        )
        server.add_insecure_port("[::]:50051")
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)
