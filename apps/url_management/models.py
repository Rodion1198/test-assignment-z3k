import uuid
from django.db import models
from django.contrib.auth.models import User

from apps.url_management.utils import generate_redirect_identifier


class RedirectRule(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Modified"
    )
    redirect_url = models.URLField(
        verbose_name="Redirect URL",
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name="Is Private",
    )
    redirect_identifier = models.CharField(
        max_length=100,
        default=generate_redirect_identifier,
        unique=True,
        editable=False,
        verbose_name="Redirect Identifier",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Owner",
    )

    class Meta:
        verbose_name = "Redirect Rule"
        verbose_name_plural = "Redirect Rules"
        ordering = ["-created"]

    def __str__(self):
        return (f"[{'Private' if self.is_private else 'Public'}] {self.redirect_identifier} "
                f"---> {self.redirect_url} (Owner: {self.owner.username})")
