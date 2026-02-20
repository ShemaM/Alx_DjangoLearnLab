from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications_sent",
    )
    verb = models.CharField(max_length=255)

    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    target_object_id = models.PositiveBigIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("is_read", "-timestamp")
        indexes = [
            models.Index(fields=["recipient", "is_read", "-timestamp"]),
        ]

    def __str__(self) -> str:
        return f"{self.recipient} - {self.actor} {self.verb}"

    @classmethod
    def create(cls, *, recipient, actor, verb: str, target=None):
        if target is None:
            return cls.objects.create(recipient=recipient, actor=actor, verb=verb)
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target_content_type=ContentType.objects.get_for_model(target),
            target_object_id=target.pk,
        )

