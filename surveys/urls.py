from django.conf.urls import url
# from surveys.views import HomeView

import views


app_name = 'surveys'
urlpatterns = [
    url(r'^$',  views.HomeView.as_view(), name='home'),
    url(r'^about/$',  views.AboutView.as_view(), name='about'),
    url(r'^blog/$',  views.BlogView.as_view(), name='blog'),
    url(r'^privacy-policy/$',  views.PrivacyView.as_view(), name='privacypolicy'),
    url(r'^pricing/$',  views.PricingView.as_view(), name='pricing'),
    # url(r'^survey-form/$',  views.pricing, name='survey-form'),

    url(r'^sign-up/$',  views.SignupView.as_view(), name='signup'),
    url(r'^success/$',  views.SuccessView.as_view(), name='success'),
    url(r'^thanks/$',  views.ThanksView.as_view()),
    # url(r'^contact/$',  views.contact, name='contact'),
    # ex: /survey/5/
    url(r'^survey/(?P<survey_pk>[0-9]+)/$', views.SurveyView.as_view(), name='survey'),

    # url(r'^survey/(?P<pk>[0-9]+)', SurveyView.as_view(), name='survey'),
]
