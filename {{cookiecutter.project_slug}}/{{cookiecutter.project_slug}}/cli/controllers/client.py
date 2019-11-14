import uuid

import cement
import grpc

from sentieo.proto.{{ cookiecutter.project_slug }}.type import file_pb2
from sentieo.proto.{{ cookiecutter.project_slug }}.v1 import convert_pb2, convert_pb2_grpc


class O3Client(cement.Controller):
    class Meta:
        label = "client"
        stacked_type = "nested"

    def __init__(self, *args, **kwargs):
        super(O3Client, self).__init__(*args, **kwargs)

        self._conversion_service = None

    @property
    def service(self):
        if not self._conversion_service:
            channel = grpc.insecure_channel("localhost:50051")
            self._conversion_service = convert_pb2_grpc.FileConversionStub(
                channel
            )

        return self._conversion_service

    @cement.ex(description="Sends a file for conversion.")
    def send(self):
        def streaming_request_messages():
            source_params = convert_pb2.SourceParameters()
            source_params.request_id = str(uuid.uuid4())
            source_params.source_system = "O3 Client"

            file_metadata = file_pb2.FileMetadata(
                name="112.xls",
                format=file_pb2.FileMetadata.XLS,
                content_type="application/vnd.ms-excel",
            )

            conversion_config = convert_pb2.ConversionConfig(
                output_formats=[
                    convert_pb2.OutputFileFormat.TEXT,
                    convert_pb2.OutputFileFormat.HTML,
                ],
                version_tags=[convert_pb2.VersionTag.ANY],
            )

            conversion_config.source_params.CopyFrom(source_params)
            conversion_config.file_metadata.CopyFrom(file_metadata)

            yield convert_pb2.StreamingLongRunningConvertRequest(
                config=conversion_config
            )

            with open("/home/sandeep/Downloads/112.xls", "rb") as input_file:
                chunk_size = 200
                while True:
                    chunk = input_file.read(chunk_size)
                    if not chunk:
                        break

                    yield convert_pb2.StreamingLongRunningConvertRequest(
                        file_content=chunk
                    )

        convert_service = self.service
        response = convert_service.StreamingLongRunningConvert(
            streaming_request_messages()
        )

        print(convert_service.StreamingLongRunningConvert)
        print(dir(convert_service.StreamingLongRunningConvert))
        print(response.DESCRIPTOR.GetOptions())
