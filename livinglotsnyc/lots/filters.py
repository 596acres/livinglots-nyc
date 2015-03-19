from hashlib import sha1

from django.db.models import Q

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D

import django_filters
from inplace.boundaries.models import Boundary

from .models import Lot


class BoundaryFilter(django_filters.Filter):

    def filter(self, qs, value):
        name, pk = value.split('::')
        try:
            return qs.filter(
                centroid__within=Boundary.objects.get(layer__name=name, pk=pk).geometry
            )
        except Boundary.DoesNotExist:
            print 'Could not find Boundary %s %s' % (name, pk)
        return qs


class BoundingBoxFilter(django_filters.Filter):

    def filter(self, qs, value):
        bbox = Polygon.from_bbox(value.split(','))
        return qs.filter(centroid__within=bbox)


class LayerFilter(django_filters.Filter):

    def filter(self, qs, value):
        people_layers = ('in_use', 'in_use_started_here', 'organizing',)
        layers = value.split(',')
        condition = Q(lotlayer__name__in=layers)

        # Handle no_people: either no layer in people layers or layer is in
        # a selected people layer
        if 'no_people' in layers:
            condition = Q(
                ~Q(lotlayer__name__in=people_layers + ('gutterspace',)) | 
                condition
            )

        return qs.filter(condition)


class LotGroupParentFilter(django_filters.Filter):

    def filter(self, qs, value):
        if value == 'true':
            qs = qs.filter(group=None)
        return qs


class LotCenterFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        try:
            lot = Lot.objects.get(pk=value)
        except Exception:
            return qs
        return qs.filter(centroid__distance_lte=(lot.centroid, D(mi=.5)))


class OwnerFilter(django_filters.Filter):

    def __init__(self, owner_type=None, **kwargs):
        super(OwnerFilter, self).__init__(**kwargs)
        self.owner_type = owner_type

    def filter(self, qs, value):
        if not value:
            return qs
        owner_query = Q(owner__pk__in=value.split(','))
        other_owners_query = ~Q(owner__owner_type=self.owner_type)
        return qs.filter(owner_query | other_owners_query)


class OwnerTypesFilter(django_filters.Filter):

    all_owner_types = ('private_opt_in', 'public',)

    def filter(self, qs, value):
        # Exclude owners not selected, this is important for groups which might
        # live in both public and private layers
        owners = value.split(',')
        disallowed_owners = [o for o in self.all_owner_types if o not in owners]

        # Lots should also be in these layers, use layers for convenience
        return qs.filter(~Q(lotlayer__name__in=disallowed_owners),
                         lotlayer__name__in=owners)


class LotFilter(django_filters.FilterSet):

    bbox = BoundingBoxFilter()
    boundary = BoundaryFilter()
    layers = LayerFilter()
    lot_center = LotCenterFilter()
    owner_types = OwnerTypesFilter()
    parents_only = LotGroupParentFilter()
    private_owners = OwnerFilter(owner_type='private')
    public_owners = OwnerFilter(owner_type='public')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LotFilter, self).__init__(*args, **kwargs)
        # TODO adjust initial queryset based on user
        self.user = user

    def hashkey(self):
        return sha1(repr(sorted(self.data.items()))).hexdigest()

    class Meta:
        model = Lot
        fields = [
            'address_line1',
            'bbox',
            'boundary',
            'known_use',
            'layers',
            'lot_center',
            'owner_types',
            'parents_only',
            'private_owners',
            'public_owners',
        ]
