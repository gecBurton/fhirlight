from api.models.common import BaseProfile


class MedicationAdministration(BaseProfile):
    """The purpose of this profile is to describe the event of a patient consuming or otherwise being administered a
    medication. This may be as simple as swallowing a tablet, or it may be a long-running infusion.

    Related resources tie this event to the authorizing prescription, and the specific encounter between patient and
    health care practitioner."""

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-MedicationAdministration
    # Current Version	2.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource MedicationAdministration.
