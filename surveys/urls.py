from django.conf.urls import url

import views


app_name = 'surveys'
urlpatterns = [
    url(r'^$',  views.home, name='home'),
    # ex: /polls/5/
    url(r'^survey/(?P<survey_id>[0-9]+)/$', views.survey, name='survey'),
     # url(r'^survey/$',  views.survey, name='survey'),
]
