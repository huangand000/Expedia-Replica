from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^add$', views.add),
    url(r'^add_process/(?P<id>\d+)$', views.add_process),
    url(r'^travel/(?P<id>\d+)$', views.travel),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^logout$', views.logout)
]