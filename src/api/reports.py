from logging import Logger
import grpc
from injector import inject
from generated import reports_service_pb2_grpc
from src.services.reports.service import AutomatiqueReportService
from src.services.reports.schemas import GenerateAutoReportRequest


class AutoReportGeneratorServicer(reports_service_pb2_grpc.ReportGeneratorServicer):
    @inject
    def __init__(self, generator_service: AutomatiqueReportService, logger: Logger):
        self.generator_service = generator_service
        self.logger = logger

    def GenerateAutoReport(self, request, context):
        self.logger.info("Received GenerateAutoReport request")
        try:
            # Convert protobuf request to domain model

            domain_request = GenerateAutoReportRequest(text=request.text)

            # Generate report using service
            response = self.generator_service.generate_report(domain_request)
            self.logger.info("Report generated successfully")

            # Convert response back to protobuf
            from generated import reports_service_pb2

            protobuf_response = reports_service_pb2.GeneratedReports(
                report=response.report
            )
            return protobuf_response
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to generate report: {str(e)}")
            raise
