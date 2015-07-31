from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

from .models import DomainLimit
from modoboa.lib.form_utils import DynamicForm


class PlainTextWidget(forms.Widget):
    def render(self, _name, value, attrs):
        return mark_safe(
            '<p class="form-control-static">%s</p>' %
            value if value is not None else '-'
        )


class DomainLimitsForm(forms.ModelForm, DynamicForm):
    mail_limit = forms.IntegerField(
        label=ugettext_lazy("Mail limit"),
        required=False,
        help_text=ugettext_lazy(
            "Mail number limit that can contain the domain."
        )
    )
    alias_limit = forms.IntegerField(
        label=ugettext_lazy("Alias limit"),
        required=False,
        help_text=ugettext_lazy(
            "Alias number limit that can contain the domain."
        )
    )

    class Meta:
        model = DomainLimit
        fields = ('mail_limit', 'alias_limit')

    def __init__(self, *args, **kwargs):
        self.domain_limits = None
        if "instance" in kwargs:
            self.domain_limits = kwargs["instance"]

        super(DomainLimitsForm, self).__init__(*args, **kwargs)

    def save(self, request_user):
        self.instance.save()


class DomainLimitsReadonlyForm(forms.ModelForm, DynamicForm):
    mail_limit = forms.IntegerField(
        label=ugettext_lazy("Mail limit"),
        widget=PlainTextWidget,
        help_text=ugettext_lazy(
            "Mail number limit that can contain the domain."
        )
    )
    alias_limit = forms.IntegerField(
        label=ugettext_lazy("Alias limit"),
        required=False,
        widget=PlainTextWidget,
        help_text=ugettext_lazy(
            "Alias number limit that can contain the domain."
        )
    )

    class Meta:
        model = DomainLimit
        fields = ('mail_limit', 'alias_limit')

    def __init__(self, *args, **kwargs):
        self.domain_limits = None
        if "instance" in kwargs:
            self.domain_limits = kwargs["instance"]

        super(DomainLimitsReadonlyForm, self).__init__(*args, **kwargs)
