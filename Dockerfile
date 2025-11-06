# Multi-stage build with Alpine for ultra-minimal size
FROM python:3.11-alpine as builder

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache --no-dev

# Copy proto files and generate gRPC code
COPY proto ./proto
RUN mkdir -p generated && \
    .venv/bin/python -m grpc_tools.protoc \
        -I./proto \
        --python_out=./generated \
        --pyi_out=./generated \
        --grpc_python_out=./generated \
        proto/service.proto \
        proto/spelling_service.proto \
        proto/reports_service.proto \
        proto/schedule_service.proto \
        proto/pdf_service.proto && \
    sed -i 's/^import \(.*\)_pb2 as/from . import \1_pb2 as/g' generated/*_grpc.py

# Production stage
FROM python:3.11-alpine

# Create non-root user
RUN addgroup -S grpcuser && adduser -S grpcuser -G grpcuser

# Copy virtual environment and generated proto files from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/generated /app/generated

# Set working directory and copy application code
WORKDIR /app
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/logs && \
    chown -R grpcuser:grpcuser /app

# Switch to non-root user
USER grpcuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 50051

# Run the server
CMD ["python", "main.py"]