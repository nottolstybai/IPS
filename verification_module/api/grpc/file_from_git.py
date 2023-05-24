import grpc

from verification_module.api.grpc import messages_pb2, messages_pb2_grpc

def get_file_version_content(branchId, filePath, versionId):

    request = messages_pb2.GetFileVersionRequest()
    request.branchId = branchId
    request.filePath = filePath
    request.versionId = versionId

    channel = grpc.insecure_channel('localhost:50051')
    stub = messages_pb2_grpc.ProjectStub(channel)

    response = stub.GetFileVersions(request)

    return response.Versions[0].content

