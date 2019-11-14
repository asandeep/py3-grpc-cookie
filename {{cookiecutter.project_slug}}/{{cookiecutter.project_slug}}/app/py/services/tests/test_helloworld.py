import grpc
import grpc_testing
import pytest

from {{cookiecutter.protobuf_namespace}}.proto.{{cookiecutter.project_slug}}.v1 import helloworld_pb2
from {{cookiecutter.project_slug}}.app.py.services import helloworld



class TestGreeterService(object):

    @pytest.fixture
    def say_hello_rpc(self):
        greeter_service = helloworld_pb2.DESCRIPTOR.services_by_name["Greeter"]
        descriptors_to_servicers = {
            greeter_service: helloworld.GreeterServicer()
        }

        greeter_server = grpc_testing.server_from_dictionary(
            descriptors_to_servicers, grpc_testing.strict_real_time()
        )

        return greeter_server.invoke_unary_unary(
            greeter_service.methods_by_name["SayHello"], (), None,
        )

    def test_say_hello(self, say_hello_rpc):

        rpc_requests = [
            convert_pb2.StreamingLongRunningConvertRequest(
                config=conversion_config
            ),
            convert_pb2.StreamingLongRunningConvertRequest(
                file_content=file_content
            ),
        ]
        for request in rpc_requests:
            streaming_long_running_convert_rpc.send_request(request)

        streaming_long_running_convert_rpc.requests_closed()

        response, trailing_metadata, code, details = (
            streaming_long_running_convert_rpc.termination()
        )

        assert code, grpc.StatusCode.OK

        assert isinstance(response, operations_pb2.Operation)
        assert response.done is False
        assert response.WhichOneof("result") is None

        with models.SessionFactory.get_session() as session:
            request = (
                session.query(models.ConversionRequest)
                .filter(
                    models.ConversionRequest.source_system == "Unit test",
                    models.ConversionRequest.source_request_id == "test123",
                )
                .one()
            )
            assert not len(request.output_formats)
            assert not len(request.version_tags)
            assert request.persist is True

            assert request.file.name == "test.doc"
            assert not request.file.format
            assert not request.file.content_type

        mock_open.return_value.write.assert_called_once_with(file_content)
        mock_requests_post.assert_called_once()

    def test_streaming_request_no_config(
        self, streaming_long_running_convert_rpc, mocker
    ):
        mock_open = mocker.patch.object(
            conversion_servicer, "open", mocker.mock_open()
        )
        mock_requests_post = mocker.patch.object(requests, "post")

        streaming_long_running_convert_rpc.send_request(
            convert_pb2.StreamingLongRunningConvertRequest(
                file_content=fake.binary(length=10)
            )
        )

        streaming_long_running_convert_rpc.requests_closed()

        response, trailing_metadata, code, details = (
            streaming_long_running_convert_rpc.termination()
        )
        assert code == grpc.StatusCode.INVALID_ARGUMENT
        assert details == "Expected conversion config as first message."

        assert response is None

        with models.SessionFactory.get_session() as session:
            request = (
                session.query(models.ConversionRequest)
                .filter(
                    models.ConversionRequest.source_system == "Unit test",
                    models.ConversionRequest.source_request_id == "test123",
                )
                .one_or_none()
            )
            file = (
                session.query(models.File)
                .filter(models.File.name == "test.doc")
                .one_or_none()
            )
            assert request is None
            assert file is None

        mock_open.return_value.write.assert_not_called()
        mock_requests_post.assert_not_called()
