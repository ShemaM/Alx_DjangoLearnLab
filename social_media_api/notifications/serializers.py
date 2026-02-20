from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source="actor.username")
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            "id",
            "actor",
            "actor_username",
            "verb",
            "target_content_type",
            "target_object_id",
            "target_repr",
            "timestamp",
            "is_read",
        )
        read_only_fields = fields

    def get_target_repr(self, obj: Notification):
        target = getattr(obj, "target", None)
        if target is None:
            return None
        return str(target)

