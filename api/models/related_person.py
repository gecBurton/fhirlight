from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, Name, Address, ContactPoint


class RelatedPersonProfile(BaseProfile):
    """This profile allows exchange of information about a person that is involved in the care for an individual, but
    who is not the target of healthcare, nor has a formal responsibility in the care process.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-RelatedPerson
    # Current Version	2.4.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource RelatedPerson.

    patient = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="The patient this person is related to.",
        related_name="RelatedPerson_patient",
    )
    relationship = models.ManyToManyField(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_PERSON_RELATIONSHIP_TYPE
        },
        help_text="The nature of the relationship.",
    )


class RelatedPersonTelecom(ContactPoint):
    """A contact detail for the person."""

    profile = models.ForeignKey(RelatedPersonProfile, on_delete=models.CASCADE)


class RelatedPersonName(Name):
    profile = models.ForeignKey(
        RelatedPersonProfile,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )


class RelatedPersonAddress(Address):
    profile = models.ForeignKey(
        RelatedPersonProfile,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )
