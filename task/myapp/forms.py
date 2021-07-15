from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser, UserProfile, Quiz, Question, Answer, Response, QuizTakers, Comment
from django import forms


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')

class CreateTestForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ('title', 'description')

class ProfileUserForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('surname', 'yourself_information', 'photo', 'date')
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}),}

# class QuizForm(forms.Form):
#     title_anwers = forms.CharField()

# QuizForm = forms.formset_factory(QuizForm, min_num=4, validate_min=True)
class CommentCreateForm(forms.ModelForm):   

    class Meta:
        model = Comment
        fields = ('content',)

class OrderingQuizGetForm(forms.Form):
    ordering_data = forms.BooleanField(required=False)

class OrderingQuizPassing(forms.Form):
    filter_passing = forms.BooleanField(required=False)

class QuizCreateFormSet(forms.Form):
    
    title_anwers = forms.CharField(max_length=60)
    response1 = forms.CharField(max_length=60)
    response2 = forms.CharField(max_length=60)
    response3 = forms.CharField(max_length=60)
    response4 = forms.CharField(max_length=60)
    correct = forms.BooleanField()


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('correct1', 'correct2', 'correct3', 'correct4')


QuizCreateFormSet = forms.formset_factory(QuizCreateFormSet, validate_min=True)
AnswerFormSet = forms.formset_factory(AnswerForm, extra=5)
