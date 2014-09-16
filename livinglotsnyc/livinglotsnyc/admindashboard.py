from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard


class LivingLotsDashboard(Dashboard):
    columns = 3

    def __init__(self, **kwargs):

        self.children = self.children or []

        self.children.append(modules.ModelList(
            title=_('Site Content'),
            models=(
                'elephantblog.*',
                'feincms.module.page.*',
            ),
        ))

        self.children.append(modules.AppList(
            title=_('Applications'),
            exclude=(
                'django.contrib.*',
                'elephantblog.*',
                'feincms.module.page.*',
                'livinglots_usercontent.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Lot Content'),
            models=('livinglots_usercontent.*',),
        ))

        self.children.append(modules.AppList(
            title=_('Administration'),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=5
        ))
