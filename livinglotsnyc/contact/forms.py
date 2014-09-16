from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.forms import ChoiceField

from contact_form.forms import BasicContactForm


class ContactForm(BasicContactForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['reason'] = ChoiceField(choices=self.get_reason_choices())
        self.fields.keyOrder = ['name', 'email', 'reason', 'body']

    def get_reason_choices(self):
        try:
            choices = [('', 'Pick a reason'),]
            choices += [(reason, reason) for reason in settings.CONTACT_FORM_REASONS.keys()]
            return choices
        except Exception:
            raise ImproperlyConfigured('settings.CONTACT_FORM_REASONS should be a dict')

    def get_message_dict(self):
        message_dict = super(ContactForm, self).get_message_dict()
        message_dict['to'] = self.get_recipients()
        return message_dict

    def get_recipients(self):
        """
        Get recipients by submitted reason, falling back to self.recipient_list
        if anything goes wrong.
        """
        try:
            return settings.CONTACT_FORM_REASONS[self.cleaned_data['reason']]
        except Exception:
            return self.recipient_list
