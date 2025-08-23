generate-grpc:
	python -m grpc_tools.protoc \
		-I./proto \
		--python_out=./generated \
		--pyi_out=./generated \
		--grpc_python_out=./generated \
		proto/service.proto proto/spelling_service.proto

update-proto:
	git submodule update --remote --merge
