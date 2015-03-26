from django import template
from django.utils.safestring import mark_safe

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from inplace.boundaries.models import Boundary

register = template.Library()


class GetPathwayLotsLink(AsTag):
    """
    Get a link to all lots that the pathway affects.
    """
    options = Options(
        'for',
        Argument('pathway', required=True, resolve=True),
        'text',
        Argument('text', required=True, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, pathway, text):
        attributes = {}
        if pathway.specific_public_owners.exists():
            attributes['public-owner-pks'] = pathway.specific_public_owners.all().values_list('pk', flat=True)
        if pathway.specific_private_owners.exists():
            attributes['private-owner-pks'] = pathway.specific_private_owners.all().values_list('pk', flat=True)
        if pathway.borough:
            try:
                borough = Boundary.objects.get(
                    layer__name='boroughs',
                    label=pathway.borough
                )
                attributes['boundary-layer'] = 'boroughs'
                attributes['boundary-pk'] = borough.pk
            except Boundary.DoesNotExist:
                pass

        owner_types = []
        if pathway.public_owners:
            owner_types.append('public')
        if pathway.private_owners:
            owner_types.append('private_opt_in')
        attributes['owner-types'] = '[%s]' % ','.join(['"%s"' % t for t in owner_types])

        attribute_strs = ["data-%s='%s'" % (k, v) for (k, v) in attributes.items()]
        return mark_safe('<a href="#" class="map-link" %s target="_blank">%s</a>' % (
            ' '.join(attribute_strs),
            text,
        ))


register.tag(GetPathwayLotsLink)
