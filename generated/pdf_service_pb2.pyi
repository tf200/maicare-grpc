from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenerateAppointmentCardRequest(_message.Message):
    __slots__ = (
        "id",
        "client_name",
        "date",
        "mentor",
        "general_information",
        "important_contacts",
        "household_info",
        "organization_agreements",
        "youth_officer_agreements",
        "treatment_agreements",
        "smoking_rules",
        "work",
        "school_internship",
        "travel",
        "leave",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    MENTOR_FIELD_NUMBER: _ClassVar[int]
    GENERAL_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    IMPORTANT_CONTACTS_FIELD_NUMBER: _ClassVar[int]
    HOUSEHOLD_INFO_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_AGREEMENTS_FIELD_NUMBER: _ClassVar[int]
    YOUTH_OFFICER_AGREEMENTS_FIELD_NUMBER: _ClassVar[int]
    TREATMENT_AGREEMENTS_FIELD_NUMBER: _ClassVar[int]
    SMOKING_RULES_FIELD_NUMBER: _ClassVar[int]
    WORK_FIELD_NUMBER: _ClassVar[int]
    SCHOOL_INTERNSHIP_FIELD_NUMBER: _ClassVar[int]
    TRAVEL_FIELD_NUMBER: _ClassVar[int]
    LEAVE_FIELD_NUMBER: _ClassVar[int]
    id: int
    client_name: str
    date: str
    mentor: str
    general_information: _containers.RepeatedScalarFieldContainer[str]
    important_contacts: _containers.RepeatedScalarFieldContainer[str]
    household_info: _containers.RepeatedScalarFieldContainer[str]
    organization_agreements: _containers.RepeatedScalarFieldContainer[str]
    youth_officer_agreements: _containers.RepeatedScalarFieldContainer[str]
    treatment_agreements: _containers.RepeatedScalarFieldContainer[str]
    smoking_rules: _containers.RepeatedScalarFieldContainer[str]
    work: _containers.RepeatedScalarFieldContainer[str]
    school_internship: _containers.RepeatedScalarFieldContainer[str]
    travel: _containers.RepeatedScalarFieldContainer[str]
    leave: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[int] = ...,
        client_name: _Optional[str] = ...,
        date: _Optional[str] = ...,
        mentor: _Optional[str] = ...,
        general_information: _Optional[_Iterable[str]] = ...,
        important_contacts: _Optional[_Iterable[str]] = ...,
        household_info: _Optional[_Iterable[str]] = ...,
        organization_agreements: _Optional[_Iterable[str]] = ...,
        youth_officer_agreements: _Optional[_Iterable[str]] = ...,
        treatment_agreements: _Optional[_Iterable[str]] = ...,
        smoking_rules: _Optional[_Iterable[str]] = ...,
        work: _Optional[_Iterable[str]] = ...,
        school_internship: _Optional[_Iterable[str]] = ...,
        travel: _Optional[_Iterable[str]] = ...,
        leave: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GenerateAppointmentCardResponse(_message.Message):
    __slots__ = ("pdf_file_key",)
    PDF_FILE_KEY_FIELD_NUMBER: _ClassVar[int]
    pdf_file_key: str
    def __init__(self, pdf_file_key: _Optional[str] = ...) -> None: ...

class GenerateContractRequest(_message.Message):
    __slots__ = (
        "contract_id",
        "status",
        "start_date",
        "end_date",
        "reminder_period",
        "sender_name",
        "sender_address",
        "sender_contact_info",
        "client_first_name",
        "client_last_name",
        "client_address",
        "client_contact_info",
        "care_type",
        "care_name",
        "financing_act",
        "financing_option",
        "hours",
        "hours_type",
        "ambulante_display",
        "price",
        "price_time_unit",
        "vat",
        "type_name",
        "generation_date",
    )
    CONTRACT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    REMINDER_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SENDER_NAME_FIELD_NUMBER: _ClassVar[int]
    SENDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SENDER_CONTACT_INFO_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CONTACT_INFO_FIELD_NUMBER: _ClassVar[int]
    CARE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CARE_NAME_FIELD_NUMBER: _ClassVar[int]
    FINANCING_ACT_FIELD_NUMBER: _ClassVar[int]
    FINANCING_OPTION_FIELD_NUMBER: _ClassVar[int]
    HOURS_FIELD_NUMBER: _ClassVar[int]
    HOURS_TYPE_FIELD_NUMBER: _ClassVar[int]
    AMBULANTE_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    PRICE_TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    VAT_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    GENERATION_DATE_FIELD_NUMBER: _ClassVar[int]
    contract_id: int
    status: str
    start_date: str
    end_date: str
    reminder_period: int
    sender_name: str
    sender_address: str
    sender_contact_info: str
    client_first_name: str
    client_last_name: str
    client_address: str
    client_contact_info: str
    care_type: str
    care_name: str
    financing_act: str
    financing_option: str
    hours: float
    hours_type: str
    ambulante_display: str
    price: float
    price_time_unit: str
    vat: float
    type_name: str
    generation_date: str
    def __init__(
        self,
        contract_id: _Optional[int] = ...,
        status: _Optional[str] = ...,
        start_date: _Optional[str] = ...,
        end_date: _Optional[str] = ...,
        reminder_period: _Optional[int] = ...,
        sender_name: _Optional[str] = ...,
        sender_address: _Optional[str] = ...,
        sender_contact_info: _Optional[str] = ...,
        client_first_name: _Optional[str] = ...,
        client_last_name: _Optional[str] = ...,
        client_address: _Optional[str] = ...,
        client_contact_info: _Optional[str] = ...,
        care_type: _Optional[str] = ...,
        care_name: _Optional[str] = ...,
        financing_act: _Optional[str] = ...,
        financing_option: _Optional[str] = ...,
        hours: _Optional[float] = ...,
        hours_type: _Optional[str] = ...,
        ambulante_display: _Optional[str] = ...,
        price: _Optional[float] = ...,
        price_time_unit: _Optional[str] = ...,
        vat: _Optional[float] = ...,
        type_name: _Optional[str] = ...,
        generation_date: _Optional[str] = ...,
    ) -> None: ...

class GenerateContractResponse(_message.Message):
    __slots__ = ("pdf_file_key",)
    PDF_FILE_KEY_FIELD_NUMBER: _ClassVar[int]
    pdf_file_key: str
    def __init__(self, pdf_file_key: _Optional[str] = ...) -> None: ...

class GenerateIncidentReportRequest(_message.Message):
    __slots__ = (
        "id",
        "employee_id",
        "employee_first_name",
        "employee_last_name",
        "location_id",
        "reporter_involvement",
        "inform_who",
        "incident_date",
        "runtime_incident",
        "incident_type",
        "passing_away",
        "self_harm",
        "violence",
        "fire_water_damage",
        "accident",
        "client_absence",
        "medicines",
        "organization",
        "use_prohibited_substances",
        "other_notifications",
        "severity_of_incident",
        "incident_explanation",
        "recurrence_risk",
        "incident_prevent_steps",
        "incident_taken_measures",
        "technical",
        "organizational",
        "mese_worker",
        "client_options",
        "other_cause",
        "cause_explanation",
        "physical_injury",
        "physical_injury_desc",
        "psychological_damage",
        "psychological_damage_desc",
        "needed_consultation",
        "succession",
        "succession_desc",
        "other",
        "other_desc",
        "additional_appointments",
        "employee_absenteeism",
        "client_id",
        "client_firstname",
        "client_lastname",
        "location_name",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    EMPLOYEE_ID_FIELD_NUMBER: _ClassVar[int]
    EMPLOYEE_FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    EMPLOYEE_LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    REPORTER_INVOLVEMENT_FIELD_NUMBER: _ClassVar[int]
    INFORM_WHO_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_DATE_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PASSING_AWAY_FIELD_NUMBER: _ClassVar[int]
    SELF_HARM_FIELD_NUMBER: _ClassVar[int]
    VIOLENCE_FIELD_NUMBER: _ClassVar[int]
    FIRE_WATER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    ACCIDENT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ABSENCE_FIELD_NUMBER: _ClassVar[int]
    MEDICINES_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    USE_PROHIBITED_SUBSTANCES_FIELD_NUMBER: _ClassVar[int]
    OTHER_NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_OF_INCIDENT_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_EXPLANATION_FIELD_NUMBER: _ClassVar[int]
    RECURRENCE_RISK_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_PREVENT_STEPS_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_TAKEN_MEASURES_FIELD_NUMBER: _ClassVar[int]
    TECHNICAL_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATIONAL_FIELD_NUMBER: _ClassVar[int]
    MESE_WORKER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    OTHER_CAUSE_FIELD_NUMBER: _ClassVar[int]
    CAUSE_EXPLANATION_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_INJURY_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_INJURY_DESC_FIELD_NUMBER: _ClassVar[int]
    PSYCHOLOGICAL_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    PSYCHOLOGICAL_DAMAGE_DESC_FIELD_NUMBER: _ClassVar[int]
    NEEDED_CONSULTATION_FIELD_NUMBER: _ClassVar[int]
    SUCCESSION_FIELD_NUMBER: _ClassVar[int]
    SUCCESSION_DESC_FIELD_NUMBER: _ClassVar[int]
    OTHER_FIELD_NUMBER: _ClassVar[int]
    OTHER_DESC_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_APPOINTMENTS_FIELD_NUMBER: _ClassVar[int]
    EMPLOYEE_ABSENTEEISM_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_LASTNAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    employee_id: int
    employee_first_name: str
    employee_last_name: str
    location_id: int
    reporter_involvement: str
    inform_who: _containers.RepeatedScalarFieldContainer[str]
    incident_date: str
    runtime_incident: str
    incident_type: str
    passing_away: bool
    self_harm: bool
    violence: bool
    fire_water_damage: bool
    accident: bool
    client_absence: bool
    medicines: bool
    organization: bool
    use_prohibited_substances: bool
    other_notifications: bool
    severity_of_incident: str
    incident_explanation: str
    recurrence_risk: str
    incident_prevent_steps: str
    incident_taken_measures: str
    technical: _containers.RepeatedScalarFieldContainer[str]
    organizational: _containers.RepeatedScalarFieldContainer[str]
    mese_worker: _containers.RepeatedScalarFieldContainer[str]
    client_options: _containers.RepeatedScalarFieldContainer[str]
    other_cause: str
    cause_explanation: str
    physical_injury: str
    physical_injury_desc: str
    psychological_damage: str
    psychological_damage_desc: str
    needed_consultation: str
    succession: _containers.RepeatedScalarFieldContainer[str]
    succession_desc: str
    other: bool
    other_desc: str
    additional_appointments: str
    employee_absenteeism: str
    client_id: int
    client_firstname: str
    client_lastname: str
    location_name: str
    def __init__(
        self,
        id: _Optional[int] = ...,
        employee_id: _Optional[int] = ...,
        employee_first_name: _Optional[str] = ...,
        employee_last_name: _Optional[str] = ...,
        location_id: _Optional[int] = ...,
        reporter_involvement: _Optional[str] = ...,
        inform_who: _Optional[_Iterable[str]] = ...,
        incident_date: _Optional[str] = ...,
        runtime_incident: _Optional[str] = ...,
        incident_type: _Optional[str] = ...,
        passing_away: bool = ...,
        self_harm: bool = ...,
        violence: bool = ...,
        fire_water_damage: bool = ...,
        accident: bool = ...,
        client_absence: bool = ...,
        medicines: bool = ...,
        organization: bool = ...,
        use_prohibited_substances: bool = ...,
        other_notifications: bool = ...,
        severity_of_incident: _Optional[str] = ...,
        incident_explanation: _Optional[str] = ...,
        recurrence_risk: _Optional[str] = ...,
        incident_prevent_steps: _Optional[str] = ...,
        incident_taken_measures: _Optional[str] = ...,
        technical: _Optional[_Iterable[str]] = ...,
        organizational: _Optional[_Iterable[str]] = ...,
        mese_worker: _Optional[_Iterable[str]] = ...,
        client_options: _Optional[_Iterable[str]] = ...,
        other_cause: _Optional[str] = ...,
        cause_explanation: _Optional[str] = ...,
        physical_injury: _Optional[str] = ...,
        physical_injury_desc: _Optional[str] = ...,
        psychological_damage: _Optional[str] = ...,
        psychological_damage_desc: _Optional[str] = ...,
        needed_consultation: _Optional[str] = ...,
        succession: _Optional[_Iterable[str]] = ...,
        succession_desc: _Optional[str] = ...,
        other: bool = ...,
        other_desc: _Optional[str] = ...,
        additional_appointments: _Optional[str] = ...,
        employee_absenteeism: _Optional[str] = ...,
        client_id: _Optional[int] = ...,
        client_firstname: _Optional[str] = ...,
        client_lastname: _Optional[str] = ...,
        location_name: _Optional[str] = ...,
    ) -> None: ...

class GenerateIncidentReportResponse(_message.Message):
    __slots__ = ("pdf_file_key",)
    PDF_FILE_KEY_FIELD_NUMBER: _ClassVar[int]
    pdf_file_key: str
    def __init__(self, pdf_file_key: _Optional[str] = ...) -> None: ...

class InvoicePeriod(_message.Message):
    __slots__ = (
        "start_date",
        "end_date",
        "accommodation_time_frame",
        "ambulante_total_minutes",
    )
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    ACCOMMODATION_TIME_FRAME_FIELD_NUMBER: _ClassVar[int]
    AMBULANTE_TOTAL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    start_date: str
    end_date: str
    accommodation_time_frame: str
    ambulante_total_minutes: float
    def __init__(
        self,
        start_date: _Optional[str] = ...,
        end_date: _Optional[str] = ...,
        accommodation_time_frame: _Optional[str] = ...,
        ambulante_total_minutes: _Optional[float] = ...,
    ) -> None: ...

class InvoiceDetail(_message.Message):
    __slots__ = (
        "care_type",
        "periods",
        "price",
        "price_time_unit",
        "pre_vat_total",
        "total",
    )
    CARE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PERIODS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    PRICE_TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    PRE_VAT_TOTAL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    care_type: str
    periods: _containers.RepeatedCompositeFieldContainer[InvoicePeriod]
    price: float
    price_time_unit: str
    pre_vat_total: float
    total: float
    def __init__(
        self,
        care_type: _Optional[str] = ...,
        periods: _Optional[_Iterable[_Union[InvoicePeriod, _Mapping]]] = ...,
        price: _Optional[float] = ...,
        price_time_unit: _Optional[str] = ...,
        pre_vat_total: _Optional[float] = ...,
        total: _Optional[float] = ...,
    ) -> None: ...

class GenerateInvoicePdfRequest(_message.Message):
    __slots__ = (
        "id",
        "sender_name",
        "sender_contact_person",
        "sender_address_line1",
        "sender_postal_code_city",
        "invoice_number",
        "invoice_date",
        "due_date",
        "invoice_details",
        "total_amount",
        "extra_items",
    )
    class ExtraItemsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_NAME_FIELD_NUMBER: _ClassVar[int]
    SENDER_CONTACT_PERSON_FIELD_NUMBER: _ClassVar[int]
    SENDER_ADDRESS_LINE1_FIELD_NUMBER: _ClassVar[int]
    SENDER_POSTAL_CODE_CITY_FIELD_NUMBER: _ClassVar[int]
    INVOICE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    INVOICE_DATE_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    INVOICE_DETAILS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EXTRA_ITEMS_FIELD_NUMBER: _ClassVar[int]
    id: int
    sender_name: str
    sender_contact_person: str
    sender_address_line1: str
    sender_postal_code_city: str
    invoice_number: str
    invoice_date: str
    due_date: str
    invoice_details: _containers.RepeatedCompositeFieldContainer[InvoiceDetail]
    total_amount: float
    extra_items: _containers.ScalarMap[str, str]
    def __init__(
        self,
        id: _Optional[int] = ...,
        sender_name: _Optional[str] = ...,
        sender_contact_person: _Optional[str] = ...,
        sender_address_line1: _Optional[str] = ...,
        sender_postal_code_city: _Optional[str] = ...,
        invoice_number: _Optional[str] = ...,
        invoice_date: _Optional[str] = ...,
        due_date: _Optional[str] = ...,
        invoice_details: _Optional[_Iterable[_Union[InvoiceDetail, _Mapping]]] = ...,
        total_amount: _Optional[float] = ...,
        extra_items: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class GenerateInvoicePdfResponse(_message.Message):
    __slots__ = ("pdf_file_key", "size")
    PDF_FILE_KEY_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    pdf_file_key: str
    size: int
    def __init__(
        self, pdf_file_key: _Optional[str] = ..., size: _Optional[int] = ...
    ) -> None: ...
