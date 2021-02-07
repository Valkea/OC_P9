from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):

    title = models.CharField("Titre", max_length=128)

    description = models.TextField("Description", max_length=2048, blank=True)

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        "Illustration", null=True, blank=True, upload_to="%Y/%m/%d"
    )

    time_created = models.DateTimeField("Date de publication", auto_now_add=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"


class Review(models.Model):

    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
    )

    rating = models.PositiveSmallIntegerField(
        "Evaluation",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    headline = models.CharField("Titre de la revue", max_length=128)

    body = models.TextField("Revue", max_length=8192, blank=True)

    time_created = models.DateTimeField("Date de publication", auto_now_add=True)

    class Meta:
        verbose_name = "Revue"
        verbose_name_plural = "Revues"
