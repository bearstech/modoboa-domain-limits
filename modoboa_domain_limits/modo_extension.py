from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext as _

from modoboa.lib import events
from modoboa.lib.exceptions import ModoboaException
from modoboa.core.extensions import ModoExtension, exts_pool

from .models import DomainLimit
from .forms import DomainLimitsForm


class MailboxLimitReached(ModoboaException):
    http_code = 403

    def __init__(self, limit):
        self.limit = limit

    def __str__(self):
        return _("Number mailbox limit %s reached") % self.limit


class MailboxAliasLimitReached(ModoboaException):
    http_code = 403

    def __init__(self, limit):
        self.limit = limit

    def __str__(self):
        return _("Number mailbox alias limit %s reached") % self.limit


@events.observe("ExtraDomainForm")
def extra_domain_form(user, domain=None):
    return [{
        'id': "domain_limits",
        'title': _("Domain limits"),
        'cls': DomainLimitsForm
    }]


@events.observe("FillDomainInstances")
def fill_domain_limits_tab(user, domain, instances):
    if not hasattr(domain, 'domainlimit'):
        domainlimit = DomainLimit(mail_limit=-1, alias_limit=-1)
        domainlimit.domain = domain
        domainlimit.save()

        domain.domainlimit = domainlimit
        domain.save()

    instances['domain_limits'] = domain.domainlimit


class DomainLimits(ModoExtension):
    name = "modoboa_domain_limits"
    label = "Domain Limits"
    version = "1.0.0"
    description = ugettext_lazy(
        "Limit the number of mail and alias by domain"
    )
    url = "domain_limits"


exts_pool.register_extension(DomainLimits)


@events.observe('MailboxCreated')
def mailbox_created(user, mailbox):
    if (
        (mailbox.domain.domainlimit.mail_limit != -1) and
        (mailbox.domain.mailbox_count > mailbox.domain.domainlimit.mail_limit)
    ):
        raise MailboxLimitReached(mailbox.domain.domainlimit.mail_limit)


@events.observe('MailboxAliasCreated')
def mailbox_alias_created(user, mailboxalias):
    if (
        (mailboxalias.domain.domainlimit.alias_limit != -1) and
        (mailboxalias.domain.mbalias_count >
            mailboxalias.domain.domainlimit.alias_limit)
    ):
        raise MailboxAliasLimitReached(
            mailboxalias.domain.domainlimit.alias_limit)
