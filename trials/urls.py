from django.conf.urls import url

from . import views

app_name = 'trials'
urlpatterns = [
    # ex: /trials/
    ##url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /trials/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /trials/5/results/
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /trials/filter/
    url(r'^$', views.SearchListView.as_view(), name='index'),
]