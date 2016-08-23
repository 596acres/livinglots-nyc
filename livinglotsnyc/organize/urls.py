from django.conf.urls import patterns, url

from livinglots import get_organizer_model
from livinglots_organize.views import AddParticipantView
import livinglots_organize.urls as llurls

from lots.models import Lot
from .forms import OrganizerForm
from .views import OrganizersJSON


urlpatterns = llurls.urlpatterns + patterns('',

    url(r'^add/',
        AddParticipantView.as_view(
            content_type_model=Lot,
            form_class=OrganizerForm,
            model=get_organizer_model(),
            object_slug_key='bbl',
            object_slug_field_name='bbl',
        ),
        name='add_organizer'),

)

standalone_urlpatterns = patterns('',
    url(r'^export/json/', OrganizersJSON.as_view(), name='export_organizers'),
)
