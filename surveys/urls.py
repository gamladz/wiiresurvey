from django.conf.urls import url

import views


app_name = 'surveys'
urlpatterns = [
    url(r'^$',  views.home, name='home'),
    url(r'^about/$',  views.about, name='about'),
    url(r'^blog/$',  views.blog, name='blog'),
    url(r'^privacy-policy/$',  views.privacypolicy, name='privacypolicy'),
    url(r'^pricing/$',  views.pricing, name='pricing'),
    url(r'^survey-form/$',  views.pricing, name='survey-form'),

    url(r'^sign-up/$',  views.success, name='signup'),
    url(r'^success/$',  views.success, name='success'),
    url(r'^thanks/$',  views.thanks),
    # url(r'^contact/$',  views.contact, name='contact'),
    # ex: /survey/5/
    url(r'^survey/(?P<survey_id>[0-9]+)/$', views.survey, name='survey'),
]
