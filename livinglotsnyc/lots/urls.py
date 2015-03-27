from django.conf.urls import patterns, url

import livinglots_lots.urls as llurls

from .views import (CountOrganizersView, CreateLotView, EmailOrganizersView,
                    LotsCountViewWithAcres, LotDetailView, LotDetailViewJSON,
                    LotsGeoJSONCentroid, LotsGeoJSONPolygon, LotsTypesOverview,
                    LotsCSV, LotsKML, LotsGeoJSON, SearchView)


urlpatterns = patterns('',

    url(r'^(?P<bbl>\d{10})/$', LotDetailView.as_view(), name='lot_detail'),
    url(r'^(?P<pk>\d+)/json/$', LotDetailViewJSON.as_view(),
        name='lot_detail_json'),
    url(r'^geojson-centroid/', LotsGeoJSONCentroid.as_view(),
        name='lot_geojson_centroid'),
    url(r'^geojson-polygon/', LotsGeoJSONPolygon.as_view(),
        name='lot_geojson_polygon'),
    url(r'^count/organizers/', CountOrganizersView.as_view(),
        name='lot_count_organizers'),
    url(r'^count/ownership/', LotsTypesOverview.as_view(),
        name='lot_ownership_overview'),
    url(r'^count/', LotsCountViewWithAcres.as_view(), name='lot_count'),
    url(r'^csv/', LotsCSV.as_view(), name='csv'),
    url(r'^kml/', LotsKML.as_view(), name='kml'),
    url(r'^geojson/', LotsGeoJSON.as_view(), name='geojson'),

    url(r'^search/', SearchView.as_view(), name='search'),

    url(r'^create/by-parcels/$', CreateLotView.as_view(),
        name='create_by_parcels'),

    url(r'^organizers/email/', EmailOrganizersView.as_view(),
        name='lot_email_organizers'),

) + llurls.urlpatterns
