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

def signup(request):
    return render(request, 'surveys/signup.html', {})

def privacypolicy(request):
    return render(request, 'surveys/privacypolicy.html', {})

def pricing(request):
    return render(request, 'surveys/pricing.html', {})

def survey(request, survey_id):
    return render(request, 'surveys/survey.html', {})

def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['gameli.ladzekpo@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')


def get_signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            recipients = ['gameli.ladzekpo@gmail.com']
            recipients.append(from_email)

            send_mail(subject, message, from_email, recipients)
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'surveys/signup.html', {'form': form})
