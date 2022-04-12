from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Attendence(models.Model):
    date = models.DateField(_("Date"), auto_now=False, auto_now_add=True)
    attendees = models.ManyToManyField("authentication.CustomUser", verbose_name=_("Attendes"))
