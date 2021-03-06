from braces.views import FormValidMessageMixin
from contact_form.views import ContactFormView as _ContactFormView
from feincms.content.application.models import app_reverse

from newsletter.subscribe import subscribe

from .forms import ContactForm


class ContactFormView(FormValidMessageMixin, _ContactFormView):
    form_class = ContactForm
    template_name = 'contact_form/form.html'

    def form_valid(self, form):
        subscribe(form.cleaned_data['email'],
                  full_name=form.cleaned_data['name'])
        super(ContactFormView, self).form_valid(form)

    def get_form_valid_message(self):
        return 'Your message was received and you should get a response shortly.'

    def get_success_url(self):
        return app_reverse('form', 'contact_form')
