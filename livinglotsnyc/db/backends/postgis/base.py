from django.contrib.gis.db.backends.postgis.base import DatabaseWrapper \
        as PostGISDatabaseWrapper


class DatabaseWrapper(PostGISDatabaseWrapper):

    def prepare_database(self):
        """
        Override the postgis DatabaseWrapper.prepare_database() to do nothing
        unless template_postgis is set.

        This was causing issues on PostGIS < 2.0 with no template set (on
        Webfaction).
        """
        pass
