"""
Object Storage Client
S3-compatible object storage abstraction layer using boto3.

This module provides a centralized interface for object storage operations,
following the same pattern as LLMClient for consistency.
"""

from typing import Optional, Dict, Any
import io
import boto3
from botocore.exceptions import ClientError

from src.core.config import Config
from src.core.exceptions import ObjectStorageError, ConfigurationError


class ObjectStorageClient:
    """
    Wrapper for boto3 S3 client with additional functionality.

    Provides a clean interface for object storage operations with error handling,
    consistent configuration management, and support for S3-compatible services.
    """

    def __init__(self, config: Config):
        """
        Initialize Object Storage client.

        Args:
            config: Application configuration instance

        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Validate configuration
        if not config.object_storage_endpoint:
            raise ConfigurationError(
                "Object storage endpoint is required",
                config_key="object_storage_endpoint",
            )

        if not config.object_storage_key_id:
            raise ConfigurationError(
                "Object storage key ID is required", config_key="object_storage_key_id"
            )

        if not config.object_storage_key:
            raise ConfigurationError(
                "Object storage key is required", config_key="object_storage_key"
            )

        if not config.object_storage_bucket:
            raise ConfigurationError(
                "Object storage bucket is required", config_key="object_storage_bucket"
            )

        self.endpoint = config.object_storage_endpoint
        self.bucket = config.object_storage_bucket

        # Initialize boto3 S3 client
        try:
            self._client = boto3.client(
                "s3",
                endpoint_url=self.endpoint,
                aws_access_key_id=config.object_storage_key_id,
                aws_secret_access_key=config.object_storage_key,
            )
        except Exception as e:
            raise ConfigurationError(
                f"Failed to initialize object storage client: {str(e)}",
                config_key="object_storage",
                details={"endpoint": self.endpoint},
            )

    def upload_file(
        self,
        file_obj: io.BytesIO,
        key: str,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Upload a file to object storage.

        Args:
            file_obj: File-like object to upload
            object_key: Key (path) for the object in the bucket
            content_type: MIME type of the file (e.g., 'application/pdf')
            metadata: Optional metadata to attach to the object

        Returns:
            The object key of the uploaded file

        Raises:
            ObjectStorageError: If upload fails
        """
        try:
            extra_args = {}

            if content_type:
                extra_args["ContentType"] = content_type

            if metadata:
                extra_args["Metadata"] = metadata

            self._client.upload_fileobj(
                file_obj, self.bucket, key, ExtraArgs=extra_args if extra_args else None
            )

            return key

        except ClientError as e:
            raise ObjectStorageError(
                f"Failed to upload file: {str(e)}",
                operation="upload",
                bucket=self.bucket,
                key=key,
                details={"error_code": e.response.get("Error", {}).get("Code")},
            )
        except Exception as e:
            raise ObjectStorageError(
                f"Unexpected error during upload: {str(e)}",
                operation="upload",
                bucket=self.bucket,
                key=key,
            )

    def download_file(self, object_key: str) -> bytes:
        """
        Download a file from object storage.

        Args:
            object_key: Key (path) of the object to download

        Returns:
            File contents as bytes

        Raises:
            ObjectStorageError: If download fails or object not found
        """
        try:
            buffer = io.BytesIO()
            self._client.download_fileobj(self.bucket, object_key, buffer)
            buffer.seek(0)
            return buffer.read()

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")

            if error_code == "404" or error_code == "NoSuchKey":
                raise ObjectStorageError(
                    f"Object not found: {object_key}",
                    operation="download",
                    bucket=self.bucket,
                    key=object_key,
                    details={"error_code": error_code},
                )

            raise ObjectStorageError(
                f"Failed to download file: {str(e)}",
                operation="download",
                bucket=self.bucket,
                key=object_key,
                details={"error_code": error_code},
            )
        except Exception as e:
            raise ObjectStorageError(
                f"Unexpected error during download: {str(e)}",
                operation="download",
                bucket=self.bucket,
                key=object_key,
            )

    def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from object storage.

        Args:
            object_key: Key (path) of the object to delete

        Returns:
            True if deletion was successful

        Raises:
            ObjectStorageError: If deletion fails
        """
        try:
            self._client.delete_object(Bucket=self.bucket, Key=object_key)
            return True

        except ClientError as e:
            raise ObjectStorageError(
                f"Failed to delete file: {str(e)}",
                operation="delete",
                bucket=self.bucket,
                key=object_key,
                details={"error_code": e.response.get("Error", {}).get("Code")},
            )
        except Exception as e:
            raise ObjectStorageError(
                f"Unexpected error during deletion: {str(e)}",
                operation="delete",
                bucket=self.bucket,
                key=object_key,
            )

    def file_exists(self, object_key: str) -> bool:
        """
        Check if a file exists in object storage.

        Args:
            object_key: Key (path) of the object to check

        Returns:
            True if the file exists, False otherwise

        Raises:
            ObjectStorageError: If the check fails due to connection issues
        """
        try:
            self._client.head_object(Bucket=self.bucket, Key=object_key)
            return True

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")

            # 404 or NoSuchKey means the file doesn't exist
            if error_code == "404" or error_code == "NoSuchKey":
                return False

            # Other errors should be raised
            raise ObjectStorageError(
                f"Failed to check file existence: {str(e)}",
                operation="exists",
                bucket=self.bucket,
                key=object_key,
                details={"error_code": error_code},
            )
        except Exception as e:
            raise ObjectStorageError(
                f"Unexpected error during existence check: {str(e)}",
                operation="exists",
                bucket=self.bucket,
                key=object_key,
            )

    def get_file_metadata(self, object_key: str) -> Dict[str, Any]:
        """
        Get metadata for a file in object storage.

        Args:
            object_key: Key (path) of the object

        Returns:
            Dictionary containing file metadata (content-type, size, etc.)

        Raises:
            ObjectStorageError: If metadata retrieval fails or object not found
        """
        try:
            response = self._client.head_object(Bucket=self.bucket, Key=object_key)

            return {
                "content_type": response.get("ContentType"),
                "content_length": response.get("ContentLength"),
                "last_modified": response.get("LastModified"),
                "metadata": response.get("Metadata", {}),
                "etag": response.get("ETag"),
            }

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")

            if error_code == "404" or error_code == "NoSuchKey":
                raise ObjectStorageError(
                    f"Object not found: {object_key}",
                    operation="get_metadata",
                    bucket=self.bucket,
                    key=object_key,
                    details={"error_code": error_code},
                )

            raise ObjectStorageError(
                f"Failed to get file metadata: {str(e)}",
                operation="get_metadata",
                bucket=self.bucket,
                key=object_key,
                details={"error_code": error_code},
            )
        except Exception as e:
            raise ObjectStorageError(
                f"Unexpected error during metadata retrieval: {str(e)}",
                operation="get_metadata",
                bucket=self.bucket,
                key=object_key,
            )

    def generate_presigned_url(
        self, object_key: str, expiration: int = 3600, http_method: str = "GET"
    ) -> str:
        """
        Generate a presigned URL for temporary access to an object.

        Args:
            object_key: Key (path) of the object
            expiration: URL expiration time in seconds (default: 1 hour)
            http_method: HTTP method for the URL (GET, PUT, etc.)

        Returns:
            Presigned URL string

        Raises:
            ObjectStorageError: If URL generation fails
        """
        try:
            client_method = "get_object" if http_method == "GET" else "put_object"

            url = self._client.generate_presigned_url(
                client_method,
                Params={"Bucket": self.bucket, "Key": object_key},
                ExpiresIn=expiration,
            )

            return url

        except ClientError as e:
            raise ObjectStorageError(
                f"Failed to generate presigned URL: {str(e)}",
                operation="generate_url",
                bucket=self.bucket,
                key=object_key,
                details={"error_code": e.response.get("Error", {}).get("Code")},
            )
        except Exception as e:
            raise ObjectStorageError(
                f"Unexpected error during URL generation: {str(e)}",
                operation="generate_url",
                bucket=self.bucket,
                key=object_key,
            )

    def __repr__(self) -> str:
        """String representation of ObjectStorageClient."""
        return f"ObjectStorageClient(endpoint={self.endpoint}, bucket={self.bucket})"
