import grpc
import grpc_testing
import pytest

from {{cookiecutter.project_slug}}.proto.v1 import helloworld_pb2
from {{cookiecutter.project_slug}}.app.py.services import helloworld


class TestGreeterService(object):
    @pytest.fixture
    def greeter_service(self):
        return helloworld_pb2.DESCRIPTOR.services_by_name["Greeter"]

    @pytest.fixture
    def greeter_server(self, greeter_service):
        descriptors_to_servicers = {
            greeter_service: helloworld.GreeterServicer()
        }

        return grpc_testing.server_from_dictionary(
            descriptors_to_servicers, grpc_testing.strict_real_time()
        )

    def test_say_hello(self, greeter_server, greeter_service):

        hello_request = helloworld_pb2.HelloRequest()

        say_hello_rpc = greeter_server.invoke_unary_unary(
            greeter_service.methods_by_name["SayHello"], (), hello_request, None
        )

        response, trailing_metadata, code, details = say_hello_rpc.termination()

        assert code, grpc.StatusCode.OK

        assert isinstance(response, helloworld_pb2.HelloReply)
        assert response.message == "Hello, World!"

    def test_say_hello__with_name(self, greeter_server, greeter_service):

        hello_request = helloworld_pb2.HelloRequest(name="Test user")

        say_hello_rpc = greeter_server.invoke_unary_unary(
            greeter_service.methods_by_name["SayHello"], (), hello_request, None
        )

        response, trailing_metadata, code, details = say_hello_rpc.termination()

        assert code, grpc.StatusCode.OK

        assert isinstance(response, helloworld_pb2.HelloReply)
        assert response.message == "Hello, Test user!"
