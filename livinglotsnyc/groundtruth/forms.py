from django import forms

from livinglots_groundtruth.forms import GroundtruthRecordFormMixin

from .models import GroundtruthRecord


class GroundtruthRecordForm(GroundtruthRecordFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(GroundtruthRecordForm, self).__init__(*args, **kwargs)

        # Users who have permission can set the use from this form
        if not (user and user.has_perm('groundtruth.moderate_groundtruthrecord')):
            self.fields['use'].widget = forms.HiddenInput()

    class Meta:
        model = GroundtruthRecord
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
