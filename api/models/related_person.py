from django.db import models

from api.models import Patient
from api.models.common import UKCore
from api.models.datatypes import Concept, Name, Address, ContactPoint


class RelatedPerson(UKCore):
    """This profile allows exchange of information about a person that is involved in the care for an individual, but
    who is not the target of healthcare, nor has a formal responsibility in the care process.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-RelatedPerson
    # Current Version	2.4.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource RelatedPerson.

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        help_text="The patient this person is related to.",
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

    related_person = models.ForeignKey(RelatedPerson, on_delete=models.CASCADE)


class RelatedPersonName(Name):
    related_person = models.ForeignKey(
        RelatedPerson,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )


class RelatedPersonAddress(Address):
    related_person = models.ForeignKey(
        RelatedPerson,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )
