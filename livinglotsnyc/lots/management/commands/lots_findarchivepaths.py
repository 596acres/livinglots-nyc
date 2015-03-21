"""
Find archive paths for each lot, if they exist.

The archive is a snapshot of 596acres.org's lot pages that was taken before 
migration to livinglotsnyc.org.
"""
import os

from django.core.management.base import BaseCommand

from lots.models import Lot


class Command(BaseCommand):
    help = 'Find archive paths for each lot'
    args = 'basepath'

    def handle(self, basepath, *args, **options):
        print basepath
        for lot in Lot.objects.filter(archive_path=None):
            self.add_archive_path(basepath, lot)

    def add_archive_path(self, basepath, lot):
        """Add archive path to a lot starting from the given basepath."""
        for child in [c for c in lot.lots if c.bbl]:
            try:
                lot.archive_path = self.find_archive_path(basepath, child.bbl)
                if lot.archive_path:
                    lot.save()
            except Exception:
                'Failed to find archive path for %s' % child
                continue

    def find_archive_path(self, basepath, bbl):
        print 'Finding archive path for %s' % bbl
        potential_paths = (
            # Attempt to find lot/<BBL>.html path
            os.path.join('lot', '%s.html' % bbl),

            # Attempt to find lot/<BBL>/index.html path
            os.path.join('lot', bbl, 'index.html'),

            # Attempt to find en/lot/<BBL>/index.html path
            os.path.join('en', 'lot', bbl, 'index.html'),
        )

        for path in potential_paths:
            if os.path.exists(os.path.join(basepath, path)):
                # Return the relative path so we can append to a base URL later
                return path
