from django.core.urlresolvers import reverse

from livinglots_organize.models import BaseOrganizer


class Organizer(BaseOrganizer):

    def get_edit_url(self):
        return reverse('organize:edit_participant', kwargs={
            'hash': self.email_hash,
            'pk': self.object_id,
        })
