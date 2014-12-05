from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

from django import template


register = template.Library()


PLUTO_URL = 'http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#pluto'


class GetVacantReasons(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        reasons = []

        for l in lot.lots:
            if l.parcel and l.parcel.bldgclass_vacant():
                reasons.append("In <a href=\"%s\" target=\"_blank\">MapPLUTO</a> "
                               "the city lists this lot's building class as "
                               "vacant." % PLUTO_URL)
            if l.parcel and l.parcel.landuse_vacant():
                reasons.append("In <a href=\"%s\" target=\"_blank\">MapPLUTO</a> "
                               "the city lists this lot's landuse as "
                               "vacant." % PLUTO_URL)

        return list(set(reasons))


register.tag(GetVacantReasons)
