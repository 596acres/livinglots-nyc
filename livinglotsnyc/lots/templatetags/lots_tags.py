from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

from django import template


register = template.Library()


PLUTO_URL = 'http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#pluto'


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


register.tag(GetOasisUrl)
register.tag(GetVacantReasons)
