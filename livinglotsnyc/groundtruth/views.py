from livinglots import get_lot_model
from livinglots_groundtruth.views import BaseAddGroundtruthRecordView
from livinglots_lots.models import Use

from lots.views import LotBBLAddGeneric
from .forms import GroundtruthRecordForm


class AddGroundtruthRecordView(LotBBLAddGeneric, BaseAddGroundtruthRecordView):
    content_type_model = get_lot_model()
    form_class = GroundtruthRecordForm

    def get_form_kwargs(self):
        kwargs = super(AddGroundtruthRecordView, self).get_form_kwargs()
        kwargs.update({ 'user': self.request.user })
        return kwargs

    def get_initial(self):
        initial = super(AddGroundtruthRecordView, self).get_initial()
        user = self.request.user

        # If user has email / name, set that for them
        try:
            initial['contact_email'] = user.email
            initial['contact_name'] = user.first_name or user.username
        except AttributeError:
            pass

        # If user is going to be setting the use, set a default for them
        if user and user.has_perm('groundtruth.moderate_groundtruthrecord'):
            initial['actual_use'] = 'in use'
            initial['use'] = Use.objects.get(name='in use')

        return initial
