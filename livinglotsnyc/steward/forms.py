from django import forms

from livinglots_steward.forms import StewardNotificationFormMixin

from .models import StewardNotification


class StewardNotificationForm(StewardNotificationFormMixin, forms.ModelForm):

    class Meta(StewardNotificationFormMixin.Meta):
        model = StewardNotification
