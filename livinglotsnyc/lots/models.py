from pint import UnitRegistry

from django.contrib.contenttypes import generic
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from livinglots import get_stewardproject_model
from livinglots_lots.models import (BaseLot, BaseLotGroup, BaseLotLayer,
                                    BaseLotManager)

from organize.models import Organizer
from .exceptions import ParcelAlreadyInLot


ureg = UnitRegistry()


class LotManager(BaseLotManager):

    def create_lot_for_parcels(self, parcels, **lot_kwargs):
        lots = []

        # Check parcel validity
        for parcel in parcels:
            if parcel.lot_set.count():
                raise ParcelAlreadyInLot()

        # Create lots for each parcel
        for parcel in parcels:
            kwargs = {
                'parcel': parcel,
                'polygon': parcel.geom,
                'centroid': parcel.geom.centroid,
                'address_line1': parcel.address,
                'name': parcel.address,
            }
            kwargs.update(**lot_kwargs)
            lot = Lot(**kwargs)
            lot.save()
            lots.append(lot)

        # Multiple lots, create a lot group
        if len(lots) > 1:
            example_lot = lots[0]
            kwargs = {
                'address_line1': example_lot.address_line1,
                'name': example_lot.name,
            }
            kwargs.update(**lot_kwargs)
            lot = LotGroup(**kwargs)
            lot.save()
            lot.update(lots=lots)
        return lot


class LotGroupLotMixin(models.Model):

    group = models.ForeignKey('LotGroup',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('group'),
    )

    class Meta:
        abstract = True


class LotMixin(models.Model):
    BOROUGH_CHOICES = (
        ('Bronx', 'Bronx'),
        ('Brooklyn', 'Brooklyn'),
        ('Manhattan', 'Manhattan'),
        ('Queens', 'Queens'),
        ('Staten Island', 'Staten Island'),
    )

    accessible = models.BooleanField(default=True)
    bbl = models.CharField(max_length=10, unique=True, blank=True, null=True)
    block = models.IntegerField(blank=True, null=True)
    borough = models.CharField(max_length=25, choices=BOROUGH_CHOICES)
    lot_number = models.IntegerField(blank=True, null=True)
    organizers = generic.GenericRelation(Organizer)
    parcel = models.ForeignKey('parcels.Parcel',
        blank=True,
        null=True,
    )

    owner_opt_in = models.BooleanField(default=False)

    def _get_display_name(self):
        if self.name:
            return self.name
        else:
            try:
                return '%s block %d, lot %d' % (self.borough, self.block,
                                                self.lot_number)
            except TypeError:
                try:
                    blocks = list(set([l.block for l in self.lots]))
                    block_strs = []
                    for block in blocks:
                        block_strs.append('block %d, %s' % (
                            block,
                            'lots %s' % (
                                ', '.join([str(l.lot_number) for l in self.lots if l.block == block])
                            )
                        ))
                    return '%s %s' % (self.borough, '; '.join(block_strs))
                except TypeError:
                    return self.address_line1
    display_name = property(_get_display_name)

    @classmethod
    def get_filter(cls):
        from .filters import LotFilter
        return LotFilter

    def calculate_polygon_area(self):
        try:
            return self.polygon.transform(2263, clone=True).area
        except Exception:
            return None

    def _area(self):
        if not self.polygon_area:
            self.polygon_area = self.calculate_polygon_area()
            self.save()
        return self.polygon_area

    area = property(_area)

    def _area_acres(self):
        try:
            area = self.area * (ureg.feet ** 2)
            return area.to(ureg.acre).magnitude
        except ValueError:
            return None

    area_acres = property(_area_acres)

    def _owners(self):
        owners = [self.owner,] + [l.owner for l in self.lots]
        return [o for o in set(owners) if o]

    owners = property(_owners)

    def _owner_contacts(self):
        contacts = [self.owner_contact,]
        contacts += [l.owner_contact for l in self.lots]
        contacts += [l.owner.default_contact for l in self.lots if l.owner]
        return [c for c in set(contacts) if c]

    owner_contacts = property(_owner_contacts)

    def _bbox(self):
        try:
            return list(self.polygon.extent)
        except Exception:
            return None

    bbox = property(_bbox)

    def _get_lots(self):
        try:
            return self.lotgroup.lot_set.all().order_by('block', 'lot_number')
        except Exception:
            return [self,]
    lots = property(_get_lots)

    class Meta:
        abstract = True


class Lot(LotMixin, LotGroupLotMixin, BaseLot):

    objects = LotManager()

    @models.permalink
    def get_absolute_url(self):
        try:
            return ('lots:lot_detail', (), { 'pk': self.lotgroup.pk, })
        except Lot.DoesNotExist:
            return ('lots:lot_detail', (), { 'bbl': self.bbl, })

    class Meta:
        permissions = (
            ('view_preview', 'Can view preview map'),
        )


class LotGroup(BaseLotGroup, Lot):
    objects = models.Manager()


class LotLayer(BaseLotLayer):

    @classmethod
    def get_layer_filters(cls):
        started_here_pks = get_stewardproject_model().objects.filter(
            started_here=True
        ).values_list('object_id', flat=True)

        return {
            'in_use': Q(known_use__visible=True),
            'in_use_started_here': Q(
                known_use__visible=True,
                pk__in=started_here_pks
            ),
            'organizing': Q(
                known_use=None,
                organizers__post_publicly=True
            ),
            'public': Q(
                Q(known_use=None) | Q(known_use__visible=True),
                Q(
                    Q(owner__owner_type='public') |
                    Q(group=None, lotgroup__lot__owner__owner_type='public')
                )
            ),
            'private': Q(
                Q(known_use=None) | Q(known_use__visible=True),
                Q(
                    Q(owner__owner_type='private') |
                    Q(group=None, lotgroup__lot__owner__owner_type='private')
                )
            ),
            'private_opt_in': Q(
                Q(owner__owner_type='private'),
                Q(owner_opt_in=True)
            ),
            'hidden': Q(
                ~Q(known_use__name='gutterspace'),
                known_use__visible=False,
            ),
            'gutterspace': Q(known_use__name='gutterspace'),
        }
