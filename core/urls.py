from django.conf.urls import include, url

from django.urls import path
from django.contrib import admin
from django.conf import settings
import django.contrib.auth
from core import views

admin.autodiscover()

urlpatterns = [
            path('admin/', admin.site.urls),
            # Home page and profile urls
            url(r'^home/$', views.home, name='home'),
            url(r'^login/$', views.login, name='login'),
            url(r'^logout/$', views.logout, name='logout'),

            url(r'^$', views.trending, name='trending'),

            # the three feed pages
            url(r'^feed/$', views.feed, name='feed'),
            url(r'^aggregated_feed/$', views.aggregated_feed, name='aggregated_feed'),

            # a page showing the users profile
            url(r'^profile/(?P<username>[\w_-]+)/$', views.profile, name='profile'),

            # backends for follow and pin
            url(r'^pin/$', views.pin, name='pin'),
            url(r'^follow/$', views.follow, name='follow'),

            # the admin
            # url(r'^admin/', include(admin.site.urls)),
            # url(r'^auth/', include(django.contrib.auth.urls)),
]

if settings.DEBUG:
    urlpatterns = [
                # url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                #     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                # url(r'', include('django.contrib.staticfiles.urls')),
     ] + urlpatterns

# TODO: move import verb to app when ready method.
# make sure we register verbs when django starts
from core import verbs
