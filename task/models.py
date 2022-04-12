from email.policy import default
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TaskInterns(models.Model):
    task = models.ForeignKey("task.Task", verbose_name=_("Task"), on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.CustomUser", verbose_name=_("Intern"), on_delete=models.CASCADE,db_column='user_id')

    class Meta:
        auto_created=True
        db_table = "task_taskinterns"


# Create your models here.
class Task(models.Model):
    name = models.CharField(_("Task name"), max_length=50)
    details = models.CharField(_("Details"), max_length=200)
    created_at = models.DateField(_("Date Created"), auto_now=False, auto_now_add=True)
    supervisor = models.ForeignKey("authentication.CustomUser", verbose_name=_("Supervisor"), on_delete=models.CASCADE)
    interns = models.ManyToManyField("authentication.CustomUser", verbose_name=_("Interns"), through='TaskInterns', related_name="task_obj", blank=True)
    complete = models.BooleanField(_("Is Task Complete?"), default=False)