from django.conf.urls import patterns, url

from livinglots import get_organizer_model
from livinglots_organize.forms import OrganizerForm
from livinglots_organize.views import AddParticipantView
import livinglots_organize.urls as llurls

from lots.models import Lot


urlpatterns = llurls.urlpatterns + patterns('',

    url(r'^add/',
        AddParticipantView.as_view(
            content_type_model=Lot,
            form_class=OrganizerForm,
            model=get_organizer_model(),
        ),
        name='add_organizer'),

)
