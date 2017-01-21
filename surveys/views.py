from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'surveys/home.html', {})

def survey(request, survey_id):
    return render(request, 'surveys/survey.html', {})
