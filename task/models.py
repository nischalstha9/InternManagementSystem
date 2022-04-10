from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Task(models.Model):
    name = models.CharField(_("Task name"), max_length=50)
    details = models.CharField(_("Details"), max_length=200)
    created_at = models.DateField(_("Date Created"), auto_now=False, auto_now_add=True)
    supervisor = models.ForeignKey("authentication.Supervisor", verbose_name=_("Supervisor"), on_delete=models.CASCADE)
    intern = models.ForeignKey("authentication.Intern", verbose_name=_("Intern"), on_delete=models.CASCADE)