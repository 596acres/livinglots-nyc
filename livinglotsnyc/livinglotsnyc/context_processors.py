from django.contrib.sites.models import Site


def add_domain(self):
    current_site = Site.objects.get_current()
    return {
        'domain': current_site.domain,
    }
