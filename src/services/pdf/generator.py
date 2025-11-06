from datetime import datetime
from weasyprint import HTML
from io import BytesIO
from jinja2 import Environment, FileSystemLoader, select_autoescape
from griffe import Logger
from injector import inject
from src.core.object_storage_client import ObjectStorageClient
from src.services.pdf.schema import AppointmentCardData


class PdfGeneratorService:
    @inject
    def __init__(self, object_storage_client: ObjectStorageClient, logger: Logger):
        self.object_storage_client = object_storage_client
        self.logger = logger

    def generate_appointment_card(
        self, appointment_card_data: AppointmentCardData
    ) -> BytesIO:
        """
        Generate a PDF appointment card and store it in object storage.

        Args:
            appointment_data: Data for the appointment card.

        Returns:
            URL to the stored PDF in object storage.
        """

        try:
            env = Environment(
                loader=FileSystemLoader("src/assets/templates"),
                autoescape=select_autoescape(["html", "xml"]),
            )

            template = env.get_template("appointment_card.html")
            html_content = template.render(
                client_name=appointment_card_data.client_name,
                date=appointment_card_data.date,
                mentor=appointment_card_data.mentor,
                general_information=appointment_card_data.general_information,
                important_contacts=appointment_card_data.important_contacts,
                household_info=appointment_card_data.household_info,
                organization_agreements=appointment_card_data.organization_agreements,
                youth_officer_agreements=appointment_card_data.youth_officer_agreements,
                treatment_agreements=appointment_card_data.treatment_agreements,
                smoking_rules=appointment_card_data.smoking_rules,
                work=appointment_card_data.work,
                school_internship=appointment_card_data.school_internship,
                travel=appointment_card_data.travel,
                leave=appointment_card_data.leave,
            )

            pdf_file = BytesIO()
            HTML(string=html_content).write_pdf(pdf_file)
            pdf_file.seek(0)
            return pdf_file
        except Exception as e:
            raise Exception(f"PDF generation error: {str(e)}")

    def upload_pdf(self, appointment_card_data: AppointmentCardData) -> str:
        """
        Upload the generated PDF to object storage.

        Args:
            pdf_file: In-memory PDF file.
            filename: Desired filename in object storage.

        Returns:
            URL to the stored PDF.
        """
        try:
            pdf_file = self.generate_appointment_card(appointment_card_data)
            filename = f"appointment_cards/{datetime.now().strftime('%Y-%m-%d')}/appointment_card_{str(appointment_card_data.id)}.pdf"
            key = self.object_storage_client.upload_file(
                file_obj=pdf_file, key=filename, content_type="application/pdf"
            )
            return key
        except Exception as e:
            raise Exception(f"PDF upload error: {str(e)}")
