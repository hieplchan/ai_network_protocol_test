https://developers.google.com/protocol-buffers/docs/kotlintutorial
https://github.com/protocolbuffers/protobuf/blob/master/src/README.md

protoc -I=. --kotlin_out=./android_client/app/src/main/proto ./imageprocess.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./imageprocess.proto

https://grpc.io/docs/languages/kotlin/quickstart/