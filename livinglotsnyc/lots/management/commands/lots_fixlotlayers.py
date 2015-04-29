"""
Fix LotLayers for each Lot in the system.

Usually when a Lot is saved, its LotLayer memberships are automatically 
updated using a signal. There are some changes that do not trigger a check for
LotLayers, though, such as when an Owner's type changes or when Lots are 
updated in bulk.

This can have serious detrimental effects on the map since Lots will show up
with an incorrect owner, on the wrong layer (eg public vs private), or might
not show up at all. This is intentional--some Owners have thousands of Lots,
and updating each one during a request could be so slow that it would timeout.

So here we will load every Lot individually and save it, thus triggering an
update on the LotLayers.
"""
from django.core.management.base import BaseCommand

from lots.models import Lot


class Command(BaseCommand):
    help = 'Fix LotLayer memberships for each Lot'

    def handle(self, *args, **options):
        for lot in Lot.objects.all():
            lot.save()
