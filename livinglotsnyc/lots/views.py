from collections import OrderedDict
import geojson
import json
from operator import itemgetter
from pint import UnitRegistry
from random import shuffle

from django.db.models import Count, Sum, Q
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from braces.views import (CsrfExemptMixin, JSONResponseMixin, LoginRequiredMixin,
                          PermissionRequiredMixin)
from caching.base import cached

from inplace.views import GeoJSONListView
from livinglots_genericviews.views import JSONResponseView
from livinglots_lots.views import BaseCreateLotView
from livinglots_lots.views import FilteredLotsMixin, LotsCountView
from livinglots_lots.views import LotDetailView as BaseLotDetailView
from livinglots_lots.views import LotsCSV as BaseLotsCSV
from livinglots_lots.views import LotsKML as BaseLotsKML
from livinglots_lots.views import LotsGeoJSON as BaseLotsGeoJSON
from livinglots_organize.mail import mass_mail_organizers
from sizecompare.compare import find_comparable

from organize.models import Organizer
from nycdata.parcels.models import Parcel
from .models import Lot


ureg = UnitRegistry()


class LotBBLAddGeneric(object):
    object_slug_key = 'bbl'
    object_slug_field_name = 'bbl'


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


class LotDetailView(BaseLotDetailView):
    slug_field = 'bbl'
    slug_url_kwarg = 'bbl'

    def check_lot_sanity(self, request, lot):
        """
        Sanity check the lot. In particular, check for missing things every lot
        should have. Warn superusers if there is something amiss.
        """
        if not lot.centroid:
            messages.warning(request, ("This lot doesn't have a center point "
                                       "(centroid). You should edit the lot "
                                       "and add one."))
        if not lot.polygon:
            messages.warning(request, ("This lot doesn't have a shape "
                                       "(polygon). You should edit the lot "
                                       "and add one."))

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            lot = self.get_object()
            self.check_lot_sanity(request, lot)
        return super(LotDetailView, self).get(request, *args, **kwargs)


class LotDetailViewJSON(JSONResponseMixin, BaseLotDetailView):
    slug_field = 'bbl'
    slug_url_kwarg = 'bbl'

    def round_acres(self, lot):
        try:
            # Attempt to round to smallest number of digits we can
            decimal_places = 1
            rounded = 0
            area_acres = lot.area_acres
            if not area_acres:
                return None
            while not rounded:
                rounded = round(area_acres, decimal_places)
                decimal_places += 1
            return rounded
        except TypeError:
            return None

    def get(self, request, *args, **kwargs):
        lot = self.object = self.get_object()

        context = {
            'area_acres': self.round_acres(lot),
            'bbl': lot.bbl,
            'centroid': {
                'x': lot.centroid.x,
                'y': lot.centroid.y,
            },
            'name': lot.display_name,
            'number_of_lots': lot.number_of_lots,
            'part_of_group': lot.group is not None,
            'url': lot.get_absolute_url(),
        }
        if lot.owner:
            context['owner'] = lot.owner.name

        return self.render_json_response(context)


class LotsTypesOverview(FilteredLotsMixin, JSONResponseView):

    layer_labels = {
        'public': 'vacant public land',
        'private': 'private land opportunities',
        'project': 'people have access',
    }

    def get_organizing(self, qs):
        qs = qs.filter(Q(
            Q(lotlayer__name='organizing') |
            Q(lotlayer__name='in_use_started_here')
        )).distinct()
        sqft = qs.aggregate(area=Sum('polygon_area'))['area']
        if not sqft:
            sqft = 0
        return {
            'acres': self.get_acres(sqft),
            'count': qs.count(),
            'sqft': int(round(sqft)),
        }

    def get_owners(self, lots_qs):
        owners = []
        for row in lots_qs.values('owner__name').annotate(count=Count('pk'),
                                                          area=Sum('polygon_area')):
            sqft = row['area']
            try:
                sqft_display = int(round(float(sqft)))
            except TypeError:
                sqft_display = 0
            owners.append({
                'acres': self.get_acres(sqft),
                'sqft': sqft_display,
                'comparable': find_comparable(sqft),
                'count': row['count'],
                'name': row['owner__name'],
            })
        return sorted(owners, key=itemgetter('name'))

    def get_layers(self, lots):
        lots_vacant = lots.exclude(lotlayer__name__in=('in_use',
                                                       'in_use_started_here',))
        return OrderedDict((
            ('public', lots_vacant.filter(lotlayer__name='public')),
            ('private', lots_vacant.filter(lotlayer__name='private_opt_in')),
            ('project', lots.filter(lotlayer__name='in_use')),
        ))

    def get_sqft(self, qs):
        try:
            sqft = qs.aggregate(area=Sum('polygon_area'))['area']
            return int(round(sqft))
        except TypeError:
            return 0

    def get_acres(self, sqft):
        try:
            sqft = sqft * (ureg.feet ** 2)
            acres = sqft.to(ureg.acre).magnitude
            return int(round(acres))
        except (TypeError, ValueError):
            return 0

    def get_layer_counts(self, layers):
        counts = []
        for layer, qs in layers.items():
            sqft = self.get_sqft(qs.distinct())
            counts.append({
                'acres': self.get_acres(sqft),
                'comparable': find_comparable(sqft),
                'label': self.layer_labels[layer],
                'organizing': self.get_organizing(qs),
                'owners': self.get_owners(qs),
                'sqft': sqft,
                'total': qs.distinct().count(),
                'type': layer,
            })
        return counts

    def get_context_data(self, **kwargs):
        lots = self.get_lots().qs
        layers = self.get_layers(lots)
        return {
            'owners': self.get_layer_counts(layers)
        }


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
        no_known_use = lots.filter(known_use__isnull=True).distinct()
        in_use = lots.filter(known_use__isnull=False,
                             known_use__visible=True).distinct()

        context = {
            'lots-count': lots.count(),
            'lots-acres': self.get_area_in_acres(lots),
            'no-known-use-count': no_known_use.count(),
            'no-known-use-acres': self.get_area_in_acres(no_known_use),
            'in-use-count': in_use.count(),
            'in-use-acres': self.get_area_in_acres(in_use),
        }
        return context


class LotOrganizersMixin(FilteredLotsMixin):

    def get_organizers(self):
        lots = self.get_lots().qs.values_list('pk', flat=True)
        return Organizer.objects.filter(
            content_type=ContentType.objects.get_for_model(Lot),
            object_id__in=lots,
        )


class CountOrganizersView(LoginRequiredMixin, PermissionRequiredMixin,
                          JSONResponseMixin, LotOrganizersMixin, View):
    permission_required = 'lots.add_lot'

    def get(self, request, *args, **kwargs):
        organizers = self.get_organizers()
        context = {
            'emails': len(set(organizers.values_list('email', flat=True))),
            'organizers': organizers.count(),
        }
        return self.render_json_response(context)


class EmailOrganizersView(LoginRequiredMixin, PermissionRequiredMixin,
                          JSONResponseMixin, LotOrganizersMixin, View):
    permission_required = 'organize.email_organizer'

    def get(self, request, *args, **kwargs):
        organizers = self.get_organizers().exclude(email=None).exclude(email='')
        subject = request.GET.get('subject')
        text = request.GET.get('text')
        emails = set(organizers.values_list('email', flat=True))
        if not (subject and text and emails):
            return HttpResponseBadRequest('All parameters are required')
        context = {
            'emails': len(emails),
            'organizers': len(organizers),
            'subject': subject,
            'text': text,
        }

        mass_mail_organizers(subject, text, organizers)
        return self.render_json_response(context)


class LotsCSV(BaseLotsCSV):
    def get_fields(self):
        return super(LotsCSV, self).get_fields() + ('bbl', 'area_acres',)

    def get_sitename(self):
        return 'Living Lots NYC'


class LotsKML(BaseLotsKML):

    def get_sitename(self):
        return 'Living Lots NYC'


class LotsGeoJSON(BaseLotsGeoJSON):

    def get_sitename(self):
        return 'Living Lots NYC'


class CreateLotView(BaseCreateLotView):

    def get_parcels(self, pks):
        return Parcel.objects.filter(pk__in=pks)


class AddToGroupView(CsrfExemptMixin, LoginRequiredMixin, 
                     PermissionRequiredMixin, JSONResponseMixin,
                     SingleObjectMixin, View):
    model = Lot
    permission_required = 'lots.add_lot'

    def get_success_message(self, to_add):
        msg = 'Successfully added %s to this group. ' % str(to_add)
        msg += ("You're <strong>not done yet</strong>: we've merged notes, "
                "photos, organizers, and other content, but you should check "
                "on the group's owner and known use information by clicking "
                "<strong>Edit this lot</strong>.")
        return msg

    def post(self, request, *args, **kwargs):
        lot = self.get_object()
        to_add = Lot.objects.get(pk=request.POST.get('lot_to_add'))
        context = {
            'lot': lot.pk,
            'lot_to_add': to_add.pk,
            'group': lot.group_with(to_add).pk,
        }
        messages.success(request, self.get_success_message(to_add))
        return self.render_json_response(context)
