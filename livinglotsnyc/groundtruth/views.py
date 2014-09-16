from livinglots import get_lot_model
from livinglots_groundtruth.views import BaseAddGroundtruthRecordView

from .forms import GroundtruthRecordForm


class AddGroundtruthRecordView(BaseAddGroundtruthRecordView):
    content_type_model = get_lot_model()
    form_class = GroundtruthRecordForm

    def get_form_kwargs(self):
        kwargs = super(AddGroundtruthRecordView, self).get_form_kwargs()
        kwargs.update({ 'user': self.request.user })
        return kwargs
