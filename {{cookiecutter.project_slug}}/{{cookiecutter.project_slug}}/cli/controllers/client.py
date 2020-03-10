import cement
import grpc

from {{cookiecutter.project_slug}}.proto.v1 import helloworld_pb2, helloworld_pb2_grpc

class HelloworldClient(cement.Controller):
    class Meta:
        label = "client"
        stacked_type = "nested"
        description = "Hello world client."

    def __init__(self, *args, **kwargs):
        super(HelloworldClient, self).__init__(*args, **kwargs)

        self._helloworld_service = None

    @property
    def service(self):
        if not self._helloworld_service:
            channel = grpc.insecure_channel("localhost:50051")
            self._helloworld_service = helloworld_pb2_grpc.GreeterStub(
                channel
            )

        return self._helloworld_service

    @cement.ex(
        description="Sends hello request to server.",
        arguments=[
            (
                ["--from"],
                dict(
                    help="Name of person sending hello request to server",
                    action="store",
                    dest="from_name",
                ),
            )
        ])
    def hello(self):
        request = helloworld_pb2.HelloRequest()
        if self.app.pargs.from_name:
            request.name = self.app.pargs.from_name

        response = self.service.SayHello(request)
        print(response.message)
