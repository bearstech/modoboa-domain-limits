from django.db import models
from modoboa.admin.models.domain import Domain


class DomainLimit(models.Model):
    domain = models.OneToOneField(Domain)
    mail_limit = models.IntegerField(default=-1)
    alias_limit = models.IntegerField(default=-1)

    class Meta:
        db_table = 'domain_limits'
