from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from braces.views import JSONResponseMixin

from livinglots_usercontent.files.models import File
from livinglots_usercontent.notes.models import Note
from livinglots_usercontent.photos.models import Photo
from livinglots_usercontent.views import AddContentView

from lots.models import Lot
from lots.views import LotBBLAddGeneric
from .forms import FileForm, NoteForm, PhotoForm


class ContentExportView(JSONResponseMixin, ListView):

    def __init__(self, *args, **kwargs):
        super(ContentExportView, self).__init__(*args, **kwargs)
        self.base_url = 'http://%s' % Site.objects.get_current().domain

    def check_request_allowed(self, request):
        key = request.GET.get('key', None)
        if key not in settings.LLNYC_API_KEYS:
            raise PermissionDenied

    def get_content_type_string(self, content_type):
        return '.'.join(content_type.natural_key())

    def get_dicts(self):
        return [self.get_properties(o) for o in self.get_queryset()]

    def get_queryset(self):
        qs = super(ContentExportView, self).get_queryset()
        return qs.order_by('added').select_related('content_type')

    def get(self, request, *args, **kwargs):
        self.check_request_allowed(request)

        context = {
            self.model_label: self.get_dicts(),
        }
        return self.render_json_response(context)

    def get_properties(self, o):
        object_dict = {
            'pk': o.pk,
            'content_type': self.get_content_type_string(o.content_type),
            'object_id': o.object_id,
            'added': o.added,
            'added_by_name': o.added_by_name,
        }
        return object_dict


class AddFileView(LotBBLAddGeneric, AddContentView):
    content_type_model = Lot
    form_class = FileForm


class FilesJSON(ContentExportView):
    model = File
    model_label = 'files'

    def get_properties(self, o):
        object_dict = super(FilesJSON, self).get_properties(o)
        object_dict['description'] = o.description
        object_dict['document'] = self.base_url + o.document.url
        object_dict['title'] = o.title
        return object_dict


class AddNoteView(LotBBLAddGeneric, AddContentView):
    content_type_model = Lot
    form_class = NoteForm


class NotesJSON(ContentExportView):
    model = Note
    model_label = 'notes'

    def get_properties(self, o):
        object_dict = super(NotesJSON, self).get_properties(o)
        object_dict['text'] = o.text
        return object_dict


class AddPhotoView(LotBBLAddGeneric, AddContentView):
    content_type_model = Lot
    form_class = PhotoForm


class PhotosJSON(ContentExportView):
    model = Photo
    model_label = 'photos'

    def get_properties(self, o):
        object_dict = super(PhotosJSON, self).get_properties(o)
        object_dict['description'] = o.description
        object_dict['name'] = o.name
        object_dict['original_image'] = self.base_url + o.original_image.url
        return object_dict
