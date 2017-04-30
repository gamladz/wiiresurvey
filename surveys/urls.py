from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

import views


app_name = 'surveys'
urlpatterns = [
    url(r'^$',  views.HomeView.as_view(), name='home'),
    url(r'^about/$',  views.AboutView.as_view(), name='about'),
    url(r'^blog/$',  views.BlogView.as_view(), name='blog'),
    url(r'^privacy-policy/$',  views.PrivacyView.as_view(), name='privacypolicy'),
    url(r'^pricing/$',  views.PricingView.as_view(), name='pricing'),
    url(r'^demochat/$',  views.DemochatView.as_view(), name='demochat'),
    url(r'^success/$',  views.SuccessView.as_view(), name='success'),
    url(r'^thanks/$',  views.ThanksView.as_view()),
    url(r'^survey/(?P<survey_pk>[0-9]+)/$', views.SurveyView.as_view(), name='survey'),
    url(r'^surveylist/$', views.SurveyListView.as_view(), name='survey-list'),
    url(r'^survey-detail/(?P<survey_pk>[0-9]+)/$', views.SurveyDetailView.as_view(), name='survey-detail'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    ]
