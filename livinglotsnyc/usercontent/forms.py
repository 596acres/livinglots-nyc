from django import forms

from livinglots_organize.forms import NotifyParticipantsOnCreationForm
from livinglots_usercontent.files.forms import FileForm as _FileForm
from livinglots_usercontent.notes.forms import NoteForm as _NoteForm
from livinglots_usercontent.photos.forms import PhotoForm as _PhotoForm


class FileForm(NotifyParticipantsOnCreationForm, _FileForm):
    title = forms.CharField(max_length=256, required=True)


class NoteForm(NotifyParticipantsOnCreationForm, _NoteForm):
    pass


class PhotoForm(NotifyParticipantsOnCreationForm, _PhotoForm):
    pass
