from django.conf.urls import url

from map import views

urlpatterns = [
    url(r'upload', views.upload),
    url(r'world', views.world_maps),
    url(r'med-points', views.med_points),
    url(r'cases-points', views.cases_points),
    url(r'^med-point/(?P<med_point>\w{0,50})/$', views.med_point)
]