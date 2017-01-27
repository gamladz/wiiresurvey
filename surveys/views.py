from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'surveys/home.html', {})

def about(request):
    return render(request, 'surveys/about.html', {})

def blog(request):
    return render(request, 'surveys/blog.html', {})

def signup(request):
    return render(request, 'surveys/signup.html', {})

def privacypolicy(request):
    return render(request, 'surveys/privacypolicy.html', {})

def survey(request, survey_id):
    return render(request, 'surveys/survey.html', {})
