from livinglots_usercontent.views import AddContentView

from lots.models import Lot
from lots.views import LotBBLAddGeneric
from .forms import FileForm, NoteForm, PhotoForm


class AddFileView(LotBBLAddGeneric, AddContentView):
    content_type_model = Lot
    form_class = FileForm


class AddNoteView(LotBBLAddGeneric, AddContentView):
    content_type_model = Lot
    form_class = NoteForm


class AddPhotoView(LotBBLAddGeneric, AddContentView):
    content_type_model = Lot
    form_class = PhotoForm
