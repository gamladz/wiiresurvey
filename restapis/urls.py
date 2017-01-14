from django.conf.urls import url, include
from rest_framework import routers
import views


router = routers.DefaultRouter()
router.register(r'surveys', views.SurveyViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'choices', views.ChoiceViewSet)
router.register(r'responses', views.ResponseViewSet)
router.register(r'answers', views.AnswerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
