from livinglots_activities.views import BaseActivityListView


class ActivityListView(BaseActivityListView):
    paginate_by = 15
