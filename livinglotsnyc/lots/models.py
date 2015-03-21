from pint import UnitRegistry

from django.contrib.contenttypes import generic
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from livinglots import get_owner_model, get_stewardproject_model
from livinglots_lots.models import (BaseLot, BaseLotGroup, BaseLotLayer,
                                    BaseLotManager)
from nycdata.boroughs import find_borough, get_borough_number
from nycdata.bbls import build_bbl

from organize.models import Organizer


ureg = UnitRegistry()


class LotManager(BaseLotManager):

    def get_visible(self):
        # Lots are either public or private with an opt-in
        return super(LotManager, self).get_visible().filter(
            lotlayer__name__in=('public', 'private_opt_in', 'in_use')
        ).distinct()

    def find_nearby(self, lot, **kwargs):
        qs = super(LotManager, self).find_nearby(lot, **kwargs)

        # Including gutterspaces in nearby lots is annoying, remove them
        return qs.exclude(lotlayer__name='gutterspace')

    def get_lot_kwargs(self, parcel, **defaults):
        kwargs = {
            'parcel': parcel,
            'polygon': parcel.geom,
            'centroid': parcel.geom.centroid,
            'address_line1': parcel.address,
            'bbl': parcel.bbl,
            'block': parcel.block,
            'borough': parcel.borough_name,
            'lot_number': parcel.lot_number,
            'postal_code': parcel.zipcode,
            'state_province': 'NY',
        }
        kwargs.update(**defaults)

        # Create or get owner for parcels
        if parcel.ownername:
            (owner, created) = get_owner_model().objects.get_or_create(
                parcel.ownername,
                defaults={
                    'owner_type': 'private',
                }
            )
            kwargs['owner'] = owner

        return kwargs

    def fake_bbl(self, borough):
        """
        Fake a BBL for a borough.

        Return the BBL, block, and lot numbers as each is fabricated.

        XXX This is a bit silly. Every parcel in NYC has a BBL. Sometimes we
        want to map pieces of land that are not tax lots. Usually this is a
        demapped road. We want BBLs for each lot in the database as we want each
        to have a unique BBL. So we fake BBLs with a non-borough borough number
        (6), add the borough number as the block (1-5), and increment the lot
        number.
        """
        block = get_borough_number(borough)
        lot_number = 1
        try:
            fakes = self.filter(borough=borough, block=block, bbl__startswith='6')
            lot_number = fakes.order_by('-lot_number')[0].lot_number + 1
        except IndexError:
            pass
        return build_bbl(6, block, lot_number), block, lot_number

    def get_lot_kwargs_by_geom(self, geom, **defaults):
        kwargs = super(LotManager, self).get_lot_kwargs_by_geom(geom, **defaults)
        borough = find_borough(kwargs['centroid']).label
        if not borough:
            raise ValueError('Could not find a borough for this lot. Either '
                             'the lot is outside of NYC or the boroughs have '
                             'not been uploaded as boundaries.')
        bbl, block, lot = self.fake_bbl(borough)

        kwargs.update({
            'borough': borough,
            'bbl': bbl,
            'block': block,
            'lot_number': lot,
            'state_province': 'NY',
        })
        kwargs.update(**defaults)
        return kwargs

    def get_lotgroup_kwargs(self, lots, **defaults):
        kwargs = super(LotManager, self).get_lotgroup_kwargs(lots, **defaults)
        kwargs.update({
            'borough': lots[0].borough,
            'state_province': 'NY',
        })
        kwargs.update(**defaults)
        return kwargs


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
    bbl = models.CharField(max_length=10, blank=True, null=True)
    block = models.IntegerField(blank=True, null=True)
    borough = models.CharField(max_length=25, choices=BOROUGH_CHOICES)
    gutterspace = models.BooleanField(default=False)
    lot_number = models.IntegerField(blank=True, null=True)
    organizers = generic.GenericRelation(Organizer)
    parcel = models.ForeignKey('parcels.Parcel',
        blank=True,
        null=True,
    )

    files = generic.GenericRelation('files.File')
    groundtruth_records = generic.GenericRelation('groundtruth.GroundtruthRecord')
    notes = generic.GenericRelation('notes.Note')
    photos = generic.GenericRelation('photos.Photo')
    steward_notifications = generic.GenericRelation('steward.StewardNotification')
    steward_projects = generic.GenericRelation('steward.StewardProject')

    owner_opt_in = models.BooleanField(default=False)

    def _get_display_name(self):
        if self.name:
            return self.name
        if self.bbl_is_fake:
            if self.address_line1:
                return self.address_line1
            return '%s, unmapped lot #%d' % (self.borough, self.lot_number)
        try:
            return '%s block %d, lot %d' % (self.borough, self.block,
                                            self.lot_number)
        except TypeError:
            try:
                blocks = list(set([l.block for l in self.lots]))
                block_strs = []
                for block in sorted(blocks):
                    block_lots = [l for l in self.lots if l.block == block]
                    block_strs.append('block %d, %s' % (
                        block,
                        '%s %s' % (
                            'lot' if len(block_lots) == 1 else 'lots',
                            ', '.join(sorted([str(l.lot_number) for l in
                                              block_lots])),
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
            try:
                # Try to get area from parcel's PLUTO data
                self.polygon_area = self.parcel.lotarea
            except Exception:
                self.polygon_area = self.calculate_polygon_area()
            self.save()
        return self.polygon_area

    area = property(_area)

    def _area_acres(self):
        try:
            area = self.area * (ureg.feet ** 2)
            return area.to(ureg.acre).magnitude
        except (ValueError, TypeError):
            return None

    area_acres = property(_area_acres)

    def _bbl_is_fake(self):
        return self.bbl and self.bbl.startswith('6')

    bbl_is_fake = property(_bbl_is_fake)

    def _owners(self):
        owners = [self.owner,] + [l.owner for l in self.lots]
        return [o for o in set(owners) if o]

    owners = property(_owners)

    def _owner_contacts(self):
        contacts = [self.owner_contact,]
        contacts += [l.owner_contact for l in self.lots]
        contacts += [l.owner.default_contact for l in self.lots if l.owner]

        # Dedupe while keeping correct order
        return sorted(list(set(contacts)), key=contacts.index)

    owner_contacts = property(_owner_contacts)

    def _bbox(self):
        try:
            return list(self.polygon.extent)
        except Exception:
            return list(self.centroid.buffer(.0005).extent)

    bbox = property(_bbox)

    def _get_lots(self):
        try:
            return self.lotgroup.lot_set.all().order_by('block', 'lot_number')
        except Exception:
            return [self,]
    lots = property(_get_lots)

    def get_new_lotgroup_kwargs(self):
        kwargs = super(LotMixin, self).get_new_lotgroup_kwargs()
        kwargs.update({
            'borough': self.borough,
            'known_use': self.known_use,
            'known_use_certainty': self.known_use_certainty,
            'known_use_locked': self.known_use_locked,
            'steward_inclusion_opt_in': self.steward_inclusion_opt_in,
            'owner': self.owner,
            'owner_opt_in': self.owner_opt_in,
        })
        return kwargs

    def reassign_objects(self, new_lot, **kwargs):
        """Reassign related objects (eg, notes or organizers) to the new lot"""
        self.files.update(**kwargs)

        self.notes.update(**kwargs)
        self.organizers.update(**kwargs)
        self.photos.update(**kwargs)
        self.steward_projects.update(**kwargs)

        # Handle things with MonitorEntrys (moderated)
        monitor_objs = (
            list(self.groundtruth_records.all()) +
            list(self.steward_notifications.all())
        )
        for obj in monitor_objs:
            obj.content_object = new_lot
            obj.save()

    def __unicode__(self):
        if self.display_name:
            return self.display_name
        return u'%d' % self.pk

    class Meta:
        abstract = True


class VisibleLotManager(BaseLotManager):
    """A manager that only retrieves lots that are publicly viewable."""

    def get_visible(self):
        """
        Should be publicly viewable if:
            * There is no known use or its type is visible
            * The known_use_certainty is over 3
            * If any steward_projects exist, they opted in to being included
        """
        return super(VisibleLotManager, self).get_queryset().filter(
            Q(
                Q(known_use__isnull=True) |
                Q(known_use__visible=True)
            ),
            Q(
                Q(steward_projects=None) |
                Q(steward_inclusion_opt_in=True)
            ),
            Q(
                ~Q(owner__owner_type='private') |
                Q(owner_opt_in=True)
            ),
            known_use_certainty__gt=3,
            group__isnull=True,
        )

    def get_queryset(self):
        return self.get_visible()


class Lot(LotMixin, LotGroupLotMixin, BaseLot):
    objects = LotManager()
    visible = VisibleLotManager()

    @models.permalink
    def get_absolute_url(self):
        try:
            return ('lots:lot_detail', (), { 'pk': self.lotgroup.pk, })
        except Lot.DoesNotExist:
            if self.bbl:
                return ('lots:lot_detail', (), { 'bbl': self.bbl, })
            else:
                return ('lots:lot_detail', (), { 'pk': self.pk, })

    def _is_visible(self):
        # Use visible manager to avoid inconsistencies in how we define visible
        return Lot.visible.filter(pk=self.pk).exists()
    is_visible = property(_is_visible)

    class Meta:
        permissions = (
            ('view_preview', 'Can view preview map'),
        )


class LotGroup(BaseLotGroup, Lot):
    objects = models.Manager()

    class Meta:
        ordering = ['name',]


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
            'hidden': Q(known_use__visible=False),
            'gutterspace': Q(gutterspace=True),
        }
