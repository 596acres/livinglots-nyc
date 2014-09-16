from livinglots_pathways.views import BasePathwaysDetailView, BasePathwaysListView

from .models import Pathway


class PathwaysDetailView(BasePathwaysDetailView):
    model = Pathway


class PathwaysListView(BasePathwaysListView):
    model = Pathway
