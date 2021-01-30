from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserFollows(models.Model):

    user = models.ForeignKey(
            to=settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='following',
            )

    followed_user = models.ForeignKey(
            to=settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='followed_by',
            )

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )


class User(AbstractUser):
    pass
