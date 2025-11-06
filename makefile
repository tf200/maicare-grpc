generate-grpc:
	python3 -m grpc_tools.protoc \
		-I./proto \
		--python_out=./generated \
		--pyi_out=./generated \
		--grpc_python_out=./generated \
		proto/service.proto proto/spelling_service.proto proto/reports_service.proto proto/schedule_service.proto
	@echo "Fixing imports in generated gRPC files..."
	@sed -i 's/^import \(.*\)_pb2 as/from . import \1_pb2 as/g' generated/*_grpc.py

update-proto:
	git submodule update --remote --merge
