from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from .forms import ContactForm

# Create your views here.

def home(request):
    return render(request, 'surveys/home.html', {})

def about(request):
    return render(request, 'surveys/about.html', {})

def blog(request):
    return render(request, 'surveys/blog.html', {})

def privacypolicy(request):
    return render(request, 'surveys/privacypolicy.html', {})

def pricing(request):
    return render(request, 'surveys/pricing.html', {})

def survey(request, survey_id):
    return render(request, 'surveys/survey.html', {})

def success(request):
    return render(request, 'surveys/success.html', {})

def signup(request):
    return render(request, 'surveys/signup.html', {})

def thanks(request):
    return render(request, 'surveys/thanks.html', {})


def success(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            organisation = form.cleaned_data['organisation']
            name = form.cleaned_data['name']
            subject = 'Hey ' + name + ', Get Started with Wiire'
            message = 'Hi ' + name + ', thanks for stopping by. I personally reach out to everyone who visits our website. I\'ll send you an email to get started in the next day or so to get Wiire up and running with ' + organisation + '. Thanks for your interest!\n\nBe in touch soon,\n\nGam'

            from_email = form.cleaned_data['from_email']

            recipients = ['gameli.ladzekpo@gmail.com']
            recipients.append(from_email)

            send_mail(subject, message, from_email, recipients)
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'surveys/signup.html', {'form': form})
