from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

from django import template


register = template.Library()


PLUTO_URL = 'http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#pluto'


class AnyUrbanRenewalRecords(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        for l in lot.lots:
            try:
                if l.parcel and l.parcel.urbanrenewalrecord:
                    return True
            except Exception:
                continue
        return False


class GetOasisUrl(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        base = 'http://oasisnyc.net/map.aspx?etabs=1&zoomto='
        if lot.bbl and not lot.bbl_is_fake:
            return '%slot:%s' % (base, lot.bbl)
        try:
            return '%sgarden:%s' % (
                base,
                lot.steward_projects.all()[0].external_id,
            )
        except Exception:
            pass
        return None


class GetVacantReasons(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        reasons = []

        for l in tuple(lot.lots) + (lot,):
            if l.parcel and l.parcel.bldgclass_vacant():
                reasons.append("In <a href=\"%s\" target=\"_blank\">MapPLUTO</a> "
                               "the city lists this lot's building class as "
                               "vacant." % PLUTO_URL)
            if l.parcel and l.parcel.landuse_vacant():
                reasons.append("In <a href=\"%s\" target=\"_blank\">MapPLUTO</a> "
                               "the city lists this lot's landuse as "
                               "vacant." % PLUTO_URL)

            if l.added_reason == 'Drawn using add-lot mode':
                reasons.append('The lot was added manually by site admins.')

            if l.added_reason == 'Imported from GrowNYC database':
                reasons.append("The lot was imported from GrowNYC's community "
                               "gardens database")

            # Lot had help from 596
            if l.lotlayer_set.filter(name='in_use_started_here').exists():
                reasons.append('Neighbors got access to it with the help of '
                               '<a href="http://596acres.org" target="_blank">596 Acres</a>.')

        return list(set(reasons))


class UrbanRenewalDispositions(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_disposition(self, lot):
        try:
            return lot.parcel.urbanrenewalrecord.disposition_short
        except Exception:
            return None

    def get_value(self, context, lot):
        return list(set([self.get_disposition(l) for l in lot.lots \
                         if l.parcel.urbanrenewalrecord]))


class UrbanRenewalPlans(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_plan(self, lot):
        try:
            return lot.parcel.urbanrenewalrecord.plan_name
        except Exception:
            return None

    def get_value(self, context, lot):
        return list(set([self.get_plan(l) for l in lot.lots if l.parcel.urbanrenewalrecord]))


register.tag(AnyUrbanRenewalRecords)
register.tag(GetOasisUrl)
register.tag(GetVacantReasons)
register.tag(UrbanRenewalDispositions)
register.tag(UrbanRenewalPlans)
