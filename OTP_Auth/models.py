from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("profile"), on_delete=models.CASCADE)
    date_of_birth = models.DateField(_("Date of Birth"))

    def __str__(self):
        return self.user.get_full_name()
