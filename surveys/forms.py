from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from surveys.models import Survey, Question, Choice, Response, Answer

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'password1', 'password2', )


class ContactForm(forms.Form):
    organisation = forms.CharField(label='', max_length=100)
    name = forms.CharField(label='what is the message?', widget=forms.Textarea)
    from_email = forms.EmailField(label='Who is it from?')

"""class SurveyForm(forms.Form)
    question =
"""

class SurveyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey')
        super(SurveyForm, self).__init__(*args, **kwargs)

        for question in survey.questions.all():
            # converting the field name to a string
            field_name = str(question.id)
            if question.type == question.TEXT:
                field_type = forms.CharField(label=question.text,
                                             required=question.required,
                                             widget=forms.Textarea(attrs={'rows':4}))
            elif question.type == question.SELECT_ONE:
                choices = [(choice.text, choice.text) for choice in question.choices.all()]
                field_type = forms.ChoiceField(label=question.text,
                                               required=question.required,
                                               choices=choices,
                                               widget=forms.RadioSelect)
            elif question.type == question.SELECT_MULTIPLE:
                choices = [(choice.text, choice.text) for choice in question.choices.all()]
                field_type = forms.MultipleChoiceField(label=question.text,
                                                       required=question.required,
                                                       choices=choices,
                                                       widget=forms.CheckboxSelectMultiple)
            elif question.type == question.INTEGER:
                field_type = forms.IntegerField(label=question.text,
                    required=question.required)

            self.fields.update({field_name: field_type})

    def save(self, survey, responder_id):

        """
        save survey response in the Answer and Response model
        :param survey: survey object
        :param responder_id: nickname submitted with the form
        :return:
        """

        # create response
        response = Response.objects.create(
            responder_id=responder_id,
            survey=survey
        )

        # save the answers for each question
        for question in survey.questions.all():
            answer = self.cleaned_data.get(str(question.id))
            Answer.objects.create(
                body=answer,
                question=question,
                response=response
            )

