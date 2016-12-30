from django.conf.urls import url

import views


app_name = 'surveys'
urlpatterns = [
    url(r'^$',  views.home, name='home'),
]