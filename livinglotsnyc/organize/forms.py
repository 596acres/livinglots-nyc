from django import forms

from livinglots_organize.forms import OrganizerForm as BaseOrganizerForm


class OrganizerForm(BaseOrganizerForm):
    email = forms.EmailField(required=True)
