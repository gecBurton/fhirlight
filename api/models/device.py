from api.models.common import BaseProfile
from django.db import models

from api.models.datatypes import Concept, Identifier


class DeviceProfile(BaseProfile):
    """The purpose of this profile is to hold information about a type of a manufactured item that is used in the
    provision of healthcare without being substantially changed through that activity. The device may be a medical or
    non-medical device. It is referenced by other resources for recording which device performed an action such as a
    procedure or an observation, referenced when prescribing and dispensing devices for patient use or for ordering
    supplies, and used to record and transmit Unique Device Identifier (UDI) information about a device such as a
    patient's implant.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Device
    # Current Version	1.1.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Device.

    class STATUS(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"
        ENTERED_IN_ERROR = "entered-in-error"
        UNKNOWN = "unknown"

    status = models.CharField(
        max_length=16, choices=STATUS, help_text="The status of the Device."
    )
    type = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_DEVICE_TYPE},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The kind or type of device.",
        related_name="Device_type",
    )

    owner = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["organizationprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Organization responsible for device",
        related_name="Device_owner",
    )

    location = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["locationprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Where the device is found.",
        related_name="Device_location",
    )


class DeviceIdentifier(Identifier):
    """An identifier for this device."""

    system = models.URLField(
        max_length=64,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    device = models.ForeignKey(
        DeviceProfile,
        on_delete=models.CASCADE,
    )
