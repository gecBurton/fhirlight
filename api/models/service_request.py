from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept


class ServiceRequestProfile(BaseProfile):
    """This profile is a record of a request for a procedure or diagnostic or other service to be planned, proposed, or
    performed, as distinguished by the ServiceRequest.intent field value, with or on a patient.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-ServiceRequest
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource ServiceRequest.

    # ServiceRequest.category
    # ServiceRequest.priority	Indicates how quickly the ServiceRequest should be addressed with respect to other requests.

    class STATUS(models.TextChoices):
        ACTIVE = "active"
        DRAFT = "draft"
        ENTERED_IN_ERROR = "entered-in-error"
        ON_HOLD = "on-hold"
        REVOKED = "revoked"
        COMPLETED = "completed"
        UNKNOWN = "unknown"

    class INTENT(models.TextChoices):
        PROPOSAL = "proposal"
        PLAN = "plan"
        DIRECTIVE = "directive"
        ORDER = "order"
        ORIGINAL_ORDER = "original-order"
        REFLEX_ORDER = "reflex-order"
        FILLER_ORDER = "filler-order"
        INTENT_ORDER = "instance-order"
        COMPLETED = "completed"
        UNKNOWN = "unknown"
        OPTION = "option"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="The status of the order.",
    )

    basedOn = models.ManyToManyField(
        BaseProfile,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["servicerequestprofile"]},
        help_text="What request fulfills.",
        related_name="ServiceRequest_basedOn",
    )

    intent = models.CharField(
        max_length=16,
        choices=INTENT,
        help_text="Whether the request is a proposal, plan, an original order or a reflex order.",
    )

    occurrencePeriodStart = models.DateTimeField(
        null=True, blank=True, help_text="When service should start"
    )
    occurrencePeriodEnd = models.DateTimeField(
        null=True, blank=True, help_text="When service should end"
    )
    authoredOn = models.DateTimeField(
        null=True, blank=True, help_text="Date request signed"
    )

    subject = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="Individual or Entity the service is ordered for.",
        related_name="ServiceRequest_subject",
    )
    encounter = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["encounterprofile"]},
        on_delete=models.CASCADE,
        help_text="Encounter in which the request was created.",
        related_name="ServiceRequest_encounter",
    )
    requester = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        help_text="Who/what is requesting service.",
        related_name="ServiceRequest_requester",
    )
    performer = models.ManyToManyField(
        BaseProfile,
        blank=True,
        limit_choices_to={
            "polymorphic_ctype__model__in": [
                "practitionerprofile",
                "organizationprofile",
            ]
        },
        help_text="Requested performer.",
        related_name="ServiceRequest_performer",
    )
    locationReference = models.ManyToManyField(
        BaseProfile,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["locationprofile"]},
        help_text="Requested location.",
        related_name="ServiceRequest_locationReference",
    )
    reasonReference = models.ManyToManyField(
        BaseProfile,
        blank=True,
        limit_choices_to={
            "polymorphic_ctype__model__in": [
                "diagnosticreportprofile",
                "observationprofile",
            ]
        },
        help_text="Explanation/Justification for service or service",
        related_name="ServiceRequest_reasonReference",
    )
    supportingInfo = models.ManyToManyField(
        BaseProfile,
        blank=True,
        help_text="Additional clinical information",
        related_name="ServiceRequest_supportingInfo",
    )
    patientInstruction = models.TextField(
        null=True, blank=True, help_text="Patient or consumer-oriented instructions"
    )

    code = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PROCEDURE_CODE},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="What is being requested/ordered.",
        related_name="ServiceRequest_code",
    )
    reasonCode = models.ManyToManyField(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_SERVICE_REQUEST_REASON_CODE
        },
        blank=True,
        help_text="Explanation/Justification for procedure or service",
        related_name="ServiceRequest_reasonCode",
    )
    category = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_REQUEST_CATEGORY_CODE},
        blank=True,
        help_text="Classification of service",
        related_name="ServiceRequest_category",
    )

    locationCode = models.ManyToManyField(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.V3_SERVICE_DELIVERY_LOCATION_ROLE_TYPE
        },
        blank=True,
        help_text="Requested location",
        related_name="ServiceRequest_locationCode",
    )
