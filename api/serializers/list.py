from api.models.list import ListEntry, ListProfile
from api.serializers.common import BaseModelSerializer, ProfileSerializer


class ListEntrySerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = ListEntry


class ListSerializer(ProfileSerializer):
    entry = ListEntrySerializer(many=True, required=False)

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = ListProfile

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        def f(value):
            model_name = value._meta.object_name.removesuffix("Profile")
            return {"item": {"reference": f"{model_name}/{value.id}"}}

        representation["entry"] = [
            f(entry.item) for entry in ListEntry.objects.filter(profile=instance)
        ]
        return representation

    def create(self, validated_data):
        entries = validated_data.pop("entry", [])
        list_profile = super().create(validated_data)
        for entry in entries:
            ListEntry.objects.create(profile=list_profile, item=entry["item"])
        return list_profile
