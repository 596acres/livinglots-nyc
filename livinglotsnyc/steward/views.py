from livinglots import get_lot_model
from livinglots_steward.views import BaseAddStewardNotificationView

from lots.views import LotBBLAddGeneric
from .forms import StewardNotificationForm


class AddStewardNotificationView(LotBBLAddGeneric, BaseAddStewardNotificationView):
    content_type_model = get_lot_model()
    form_class = StewardNotificationForm
