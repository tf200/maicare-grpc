"""
Spelling Check gRPC Service
Thin gRPC layer for spelling correction
Migrated from: spelling_check/service.py
"""

from logging import Logger
import grpc
from injector import inject
import generated.spelling_service_pb2 as pb2
import generated.spelling_service_pb2_grpc as pb2_grpc


from src.services.spelling.corrector import SpellingCorrectorService


class SpellingCheckServicer(pb2_grpc.SpellingCorrectionServicer):
    """
    gRPC servicer for Spelling Correction.
    Thin layer that delegates to spelling service.
    """

    @inject
    def __init__(self, spelling_service: SpellingCorrectorService, logger: Logger):
        """Initialize spelling check servicer with dependencies"""
        self.spelling_service = spelling_service
        self.logger = logger
        self.logger.info("SpellingCheckServicer initialized")

    def CorrectSpelling(self, request: pb2.CorrectSpellingRequest, context):
        """
        Handle gRPC CorrectSpelling request.

        Args:
            request: CorrectSpellingRequest protobuf message
            context: gRPC context

        Returns:
            CorrectSpellingResponse protobuf message
        """
        self.logger.info("Received CorrectSpelling request")

        try:
            # Call service layer
            corrected = self.spelling_service.correct_spelling(request.initial_text)

            # Map to protobuf response
            response = pb2.CorrectSpellingResponse(
                corrected_text=corrected.corrected_text
            )

            self.logger.info("Spelling correction completed successfully")
            return response

        except Exception as e:
            self.logger.error(f"Error in CorrectSpelling: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to correct spelling: {str(e)}")
            raise
