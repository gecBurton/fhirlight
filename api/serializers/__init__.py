from .patient import PatientSerializer
from .organization import OrganizationSerializer
from .practitioner import PractitionerSerializer
from .operation_outcome import OperationOutcomeSerializer
from .questionnaire import QuestionnaireSerializer
from .slot import SlotSerializer
from .medication import MedicationSerializer
from .related_person import RelatedPersonSerializer
from .observation import ObservationSerializer
from .procedure import ProcedureSerializer
from .location import LocationSerializer
from .specimen import SpecimenSerializer
from .practitioner_role import PractitionerRoleSerializer
from .schedule import ScheduleSerializer
from .immunization import ImmunizationSerializer
from .diagnostic_report import DiagnosticReportSerializer
from .condition import ConditionSerializer
from .device import DeviceSerializer
from .consent import ConsentSerializer
from .encounter import EncounterSerializer

__all__ = [
    "ConsentSerializer",
    "DeviceSerializer",
    "ConditionSerializer",
    "PatientSerializer",
    "OrganizationSerializer",
    "PractitionerSerializer",
    "OperationOutcomeSerializer",
    "QuestionnaireSerializer",
    "SlotSerializer",
    "MedicationSerializer",
    "RelatedPersonSerializer",
    "ObservationSerializer",
    "ProcedureSerializer",
    "LocationSerializer",
    "SpecimenSerializer",
    "PractitionerRoleSerializer",
    "ScheduleSerializer",
    "ImmunizationSerializer",
    "DiagnosticReportSerializer",
]
