from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import autocomplete_light

from registration.forms import AuthenticationForm

autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
                     show_indexes=True)

urlpatterns += staticfiles_urlpatterns()

# URLs that expect to act on an individual lot
lotpatterns = patterns('',
    url(r'^content/', include('usercontent.urls', 'usercontent')),
    url(r'^groundtruth/', include('groundtruth.urls', 'groundtruth')),
    url(r'^grow-community/steward/', include('steward.urls', 'steward')),
    url(r'^grow-community/', include('organize.urls', 'organize')),
)

urlpatterns += patterns('',
    # Living Lots
    url(r'^lot/(?P<bbl>\d{10})/', include(lotpatterns)),
    url(r'^lot/', include('lots.urls', 'lots')),

    # Activity stream
    url('^activity/', include('activities.urls')),

    # Django.js
    url(r'^djangojs/', include('djangojs.urls')),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # Autocomplete
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # Auth
    url(r'^login/', 'django.contrib.auth.views.login', {
        'authentication_form': AuthenticationForm,
    }),

    # FeinCMS
    url(r'', include('feincms.urls')),
)


from django.shortcuts import render

from feincms.module.page.models import Page


def page_not_found(request, template_name='404.html'):
    page = Page.objects.best_match_for_path(request.path)
    return render(request, template_name, {'feincms_page': page}, status=404)


def error_handler(request, template_name='500.html'):
    page = Page.objects.best_match_for_path(request.path)
    return render(request, template_name, {'feincms_page': page}, status=500)


handler404 = page_not_found
handler500 = error_handler
