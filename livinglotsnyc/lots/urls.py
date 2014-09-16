from django.conf.urls import patterns, url

import livinglots_lots.urls as llurls

from .views import (LotsCountViewWithAcres, LotsGeoJSONCentroid,
                    LotsGeoJSONPolygon, LotsOwnershipOverview, LotsCSV,
                    LotsKML, LotsGeoJSON)


urlpatterns = patterns('',

    url(r'^geojson-centroid/', LotsGeoJSONCentroid.as_view(),
        name='nola_lot_geojson_centroid'),
    url(r'^geojson-polygon/', LotsGeoJSONPolygon.as_view(),
        name='lot_geojson_polygon'),
    url(r'^count/ownership/', LotsOwnershipOverview.as_view(),
        name='lot_ownership_overview'),
    url(r'^count/', LotsCountViewWithAcres.as_view(), name='lot_count'),
    url(r'^csv/', LotsCSV.as_view(), name='csv'),
    url(r'^kml/', LotsKML.as_view(), name='kml'),
    url(r'^geojson/', LotsGeoJSON.as_view(), name='geojson'),

) + llurls.urlpatterns
