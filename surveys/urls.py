from django.conf.urls import url

import views


app_name = 'surveys'
urlpatterns = [
    url(r'^$',  views.home, name='home'),
    url(r'^about/$',  views.about, name='about'),
    url(r'^blog/$',  views.blog, name='blog'),
    url(r'^sign-up/$',  views.get_signup, name='signup'),
    url(r'^privacy-policy/$',  views.privacypolicy, name='privacypolicy'),
    # url(r'^contact/$',  views.contact, name='contact'),
    # ex: /survey/5/
    url(r'^survey/(?P<survey_id>[0-9]+)/$', views.survey, name='survey'),
]
