from api.models.common import BaseProfile
from django.db import models

from api.models.datatypes import DataTypeWithPeriod


class MessageHeaderProfile(BaseProfile):
    """This profile carries the header data for a message exchange that is either requesting or responding to an action."""

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-MessageHeader
    # Current Version	2.3.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource MessageHeader.

    # Code for the event this message represents or link to event definition
    eventCodingSystem = models.URLField(
        null=True,
        blank=True,
        help_text="A selector of the type of consent being presented: ADR, Privacy, Treatment, Research.",
    )
    eventCodingDisplay = models.TextField(
        null=True,
        blank=True,
        help_text="A selector of the type of consent being presented: ADR, Privacy, Treatment, Research.",
    )
    eventCodingCode = models.CharField(
        max_length=256,
        help_text="A selector of the type of consent being presented: ADR, Privacy, Treatment, Research.",
    )

    sender = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["organizationprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Literal reference",
        related_name="MessageHeader_sender",
    )

    # The source application from which this message originated.
    sourceEndpoint = models.CharField(
        max_length=526,
        help_text="Actual message source address or id",
    )

    # The actual content of the message
    focus = models.ManyToManyField(
        BaseProfile,
        blank=True,
        help_text="The actual content of the message.",
        related_name="MessageHeader_focus",
    )


class MessageHeaderDestination(DataTypeWithPeriod):
    """The destination application which the message is intended for."""

    endpoint = models.CharField(
        max_length=526, help_text="Actual destination address or id"
    )
    receiver = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["organizationprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='Intended "real-world" recipient for the data',
        related_name="MessageHeaderDestination_receiver",
    )

    profile = models.ForeignKey(
        MessageHeaderProfile,
        on_delete=models.CASCADE,
    )
