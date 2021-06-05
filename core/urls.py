from django.conf.urls import patterns, include, url

from django.contrib.auth.views import logout, login
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from core import views

admin.autodiscover()

urlpatterns = [
    # Home page and profile urls
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^$', views.trending, name='trending'),

    # the three feed pages
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^aggregated_feed/$', views.aggregated_feed, name='aggregated_feed'),

    # admin access required
    url(r'^notification_feed/$', views.notification_feed, name='notification_feed'),

    # a page showing the users profile
    url(r'^profile/(?P<username>[\w_-]+)/$', views.profile, name='profile'),

    # backends for follow and pin
    url(r'^pin/$', views.pin, name='pin'),
    url(r'^follow/$', views.follow, name='follow'),

    # the admin
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^auth/', include('django.contrib.auth.urls')),

    # python function calls
    url(r'^seen_notification/$', views.api_notification_seen, name="seen_notification")
]

if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
     ] + urlpatterns

# TODO: move import verb to app when ready method
# make sure we register verbs when django starts
from core import verbs
