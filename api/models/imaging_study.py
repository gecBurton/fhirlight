from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, DataTypeWithPeriod


class ImagingStudyProfile(BaseProfile):
    """This profile allows exchange of the content produced in a DICOM imaging study."""

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-ImagingStudy
    # Current Version	1.0.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource ImagingStudy

    # ImagingStudy.series	Each study has one or more series of images or other content.

    class STATUS(models.TextChoices):
        REGISTERED = "registered"
        AVAILABLE = "available"
        CANCELLED = "cancelled"
        ENTERED_IN_ERROR = "entered-in-error"
        UNKNOWN = "unknown"

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        help_text="The current state of the ImagingStudy.",
    )

    subject = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="Who or what is the subject of the study.",
        related_name="ImagingReport_subject",
    )

    started = models.DateTimeField(null=True, blank=True, help_text="")
    numberOfSeries = models.PositiveIntegerField(null=True, blank=True, help_text="")
    numberOfInstances = models.PositiveIntegerField(null=True, blank=True, help_text="")

    encounter = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["encounterprofile"]},
        on_delete=models.CASCADE,
        help_text="Encounter with which this imaging study is associated",
        related_name="ImagingStudy_encounter",
    )

    modality = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_CONDITION_CATEGORY},
        blank=True,
        help_text="All series modality if actual acquisition modalities.",
        related_name="ImagingStudy_modality",
    )


class ImagingStudySeries(DataTypeWithPeriod):
    profile = models.ForeignKey(
        ImagingStudyProfile,
        on_delete=models.CASCADE,
    )

    uid = models.CharField(help_text="DICOM SOP Instance UID")
    number = models.PositiveIntegerField(
        null=True, blank=True, help_text="Numeric identifier of this series"
    )
    numberOfInstances = models.PositiveIntegerField(
        null=True, blank=True, help_text="Number of Series Related Instances"
    )
    description = models.TextField(
        null=True, blank=True, help_text="A short human readable summary of the series"
    )
    modality = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.CID_29_ACQUISITION_MODALITY},
        on_delete=models.CASCADE,
        help_text="The modality of the instances in the series",
        related_name="ImagingStudySeries_modality",
    )
    bodySite = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.SNOMED_CT_BODY_STRUCTURES},
        on_delete=models.CASCADE,
        help_text="The bodySite of the instances in the series",
        related_name="ImagingStudySeries_bodySite",
    )


class ImagingStudySeriesInstance(DataTypeWithPeriod):
    series = models.ForeignKey(
        ImagingStudySeries,
        on_delete=models.CASCADE,
    )
    uid = models.CharField(help_text="DICOM SOP Instance UID")
    sopClass = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.B5_STANDARD_SOP_CLASSES},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The modality of the instances in the series",
        related_name="ImagingStudySeriesInstance_sopClass",
    )
    number = models.PositiveIntegerField(
        null=True, blank=True, help_text="The number of this instance in the series"
    )
    title = models.CharField(
        max_length=256, null=True, blank=True, help_text="Description of instance"
    )
