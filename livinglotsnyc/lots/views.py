from collections import OrderedDict
import geojson
import json
from operator import itemgetter
from pint import UnitRegistry
from random import shuffle

from django.db.models import Count, Sum

from caching.base import cached

from inplace.views import GeoJSONListView
from livinglots_genericviews.views import JSONResponseView
from livinglots_lots.views import FilteredLotsMixin, LotsCountView
from livinglots_lots.views import LotsCSV as BaseLotsCSV
from livinglots_lots.views import LotsKML as BaseLotsKML
from livinglots_lots.views import LotsGeoJSON as BaseLotsGeoJSON


ureg = UnitRegistry()


class LotGeoJSONMixin(object):

    def get_acres(self, lot):
        acres = getattr(lot, 'area_acres', None)
        if not acres:
            return 'unknown'
        return round(acres, 2)

    def get_layer(self, lot):
        if lot.known_use:
            return 'in_use'
        elif lot.owner and lot.owner.owner_type == 'public':
            return 'public'
        elif lot.owner and lot.owner.owner_type == 'private':
            return 'private'
        return ''

    def get_properties(self, lot):
        return {
            'address_line1': lot.address_line1,
            'has_organizers': lot.organizers__count > 0,
            'layer': self.get_layer(lot),
            'number_of_lots': lot.number_of_lots,
            'number_of_lots_plural': lot.number_of_lots > 1,
            'owner': str(lot.owner) or 'unknown',
            'pk': lot.pk,
            'size': self.get_acres(lot),
        }

    def get_geometry(self, lot):
        try:
            lot_geojson = lot.geojson
        except Exception:
            if lot.polygon:
                lot_geojson = lot.polygon.geojson
            else:
                lot_geojson = lot.centroid.geojson
        return json.loads(lot_geojson)

    def get_feature(self, lot):
        return geojson.Feature(
            lot.pk,
            geometry=self.get_geometry(lot),
            properties=self.get_properties(lot),
        )


class LotsGeoJSONCentroid(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_queryset(self):
        return self.get_lots().qs.filter(centroid__isnull=False).geojson(
            field_name='centroid',
            precision=8,
        ).select_related(
            'known_use',
            'lotgroup',
            'owner__owner_type'
        ).annotate(organizers__count=Count('organizers'))

    def get_features(self):
        filterset = self.get_lots()
        key = '%s:%s' % (self.__class__.__name__, filterset.hashkey())

        def _get_value():
            features = super(LotsGeoJSONCentroid, self).get_features()
            shuffle(features)
            return features
        return cached(_get_value, key, 60 * 15)


class LotsGeoJSONPolygon(LotGeoJSONMixin, FilteredLotsMixin, GeoJSONListView):

    def get_properties(self, lot):
        properties = super(LotsGeoJSONPolygon, self).get_properties(lot)
        properties['centroid'] = (
            round(lot.centroid.x, 4),
            round(lot.centroid.y, 4)
        )
        return properties

    def get_queryset(self):
        return self.get_lots().qs.filter(polygon__isnull=False).geojson(
            field_name='polygon',
            precision=8,
        ).select_related(
            'known_use',
            'lotgroup',
            'owner__owner_type'
        ).annotate(organizers__count=Count('organizers'))

    def get_features(self):
        filterset = self.get_lots()
        key = '%s:%s' % (self.__class__.__name__, filterset.hashkey())

        def _get_value():
            return super(LotsGeoJSONPolygon, self).get_features()
        return cached(_get_value, key, 60 * 15)


class LotsOwnershipOverview(FilteredLotsMixin, JSONResponseView):

    layer_labels = {
        'public': 'publicly owned land',
        'private': 'private land belonging to an owner who wants to see it used',
    }

    def get_owners(self, lots_qs):
        owners = []
        for row in lots_qs.values('owner__name').annotate(count=Count('pk')):
            label = 'owned by %s' % row['owner__name']
            if row['owner__name'] == 'private owner':
                label = ''
            owners.append({
                'name': row['owner__name'],
                'label': label,
                'count': row['count'],
            })
        return sorted(owners, key=itemgetter('name'))

    def get_layers(self, lots):
        return OrderedDict({
            'public': lots.filter(owner__owner_type='public'),
            'private': lots.filter(
                owner__owner_type='private',
            ),
        })

    def get_layer_counts(self, layers):
        counts = []
        for layer, qs in layers.items():
            owners = self.get_owners(qs)
            if owners:
                counts.append({
                    'label': self.layer_labels[layer],
                    'owners': owners,
                    'type': layer,
                })
        return counts

    def get_context_data(self, **kwargs):
        lots = self.get_lots().qs
        layers = self.get_layers(lots)
        return self.get_layer_counts(layers)


class LotsCountViewWithAcres(LotsCountView):

    def get_area_in_acres(self, lots_qs):
        sqft = lots_qs.aggregate(total_area=Sum('polygon_area'))['total_area']
        if not sqft:
            return 0
        sqft = sqft * (ureg.feet ** 2)
        acres = sqft.to(ureg.acre).magnitude
        return int(round(acres))

    def get_context_data(self, **kwargs):
        lots = self.get_lots().qs
        no_known_use = lots.filter(known_use__isnull=True)
        in_use = lots.filter(known_use__isnull=False, known_use__visible=True)

        context = {
            'lots-count': lots.count(),
            'lots-acres': self.get_area_in_acres(lots),
            'no-known-use-count': no_known_use.count(),
            'no-known-use-acres': self.get_area_in_acres(no_known_use),
            'in-use-count': in_use.count(),
            'in-use-acres': self.get_area_in_acres(in_use),
        }
        return context


class LotsCSV(BaseLotsCSV):

    def get_sitename(self):
        # TODO replace with site name
        return ''


class LotsKML(BaseLotsKML):

    def get_sitename(self):
        # TODO replace with site name
        return ''


class LotsGeoJSON(BaseLotsGeoJSON):

    def get_sitename(self):
        # TODO replace with site name
        return ''
