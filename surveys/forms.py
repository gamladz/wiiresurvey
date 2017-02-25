from django import forms
from surveys.models import Survey, Question, Choice, Response, Answer

class ContactForm(forms.Form):
    organisation = forms.CharField(label='', max_length=100)
    name = forms.CharField(label='what is the message?', widget=forms.Textarea)
    from_email = forms.EmailField(label='Who is it from?')
