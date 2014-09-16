from livinglots_usercontent.views import AddContentView

from lots.models import Lot
from .forms import FileForm, NoteForm, PhotoForm


class AddFileView(AddContentView):
    content_type_model = Lot
    form_class = FileForm


class AddNoteView(AddContentView):
    content_type_model = Lot
    form_class = NoteForm


class AddPhotoView(AddContentView):
    content_type_model = Lot
    form_class = PhotoForm
