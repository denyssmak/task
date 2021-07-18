from django.shortcuts import render, get_object_or_404, redirect
from . import models, forms
from django.contrib.auth.views import LoginView, LogoutView
from .models import MyUser, UserProfile, Quiz, Question, Answer, Response, QuizTakers, Comment
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from .forms import (
    MyUserCreationForm, 
    CustomAuthenticationForm, 
    CreateTestForm, 
    ProfileUserForm, 
    CommentCreateForm, 
    OrderingQuizGetForm, 
    QuizCreateFormSet,
    AnswerFormSet,
    OrderingQuizPassing
)
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.db.models import Avg, Q
from django.forms.models import inlineformset_factory
from django.forms import formset_factory
import operator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url


class UserRegisterView(CreateView):
    model = MyUser
    form_class = MyUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('index')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class MainView(ListView):
    model = MyUser
    template_name = 'index.html'



def CreateTestView(request, **kwargs):
    QuizCreateFormSet = inlineformset_factory(
        models.Quiz,
        models.Question,
        fields=(
            'title_anwers', 
            'response1', 
            'correct1', 
            'response2',
            'correct2',
            'response3',
            'correct3',
            'response4',
            'correct4',
        ), 
        extra=5, 
        can_delete=False,
    )

    if request.method == 'POST':
        formset = QuizCreateFormSet(request.POST, request.FILES)
        title = request.POST.get('title')
        description = request.POST.get('description')
        form = CreateTestForm({'title': title, 'description': description })
        if form.is_valid():
            quiz = form.save()
            questions = []
            for i in range(5):
                title_anwers = request.POST.get(f'question_set-{i}-title_anwers')
                one_answer = request.POST.get(f'question_set-{i}-response{1}')
                one_correct = request.POST.get(f'question_set-{i}-correct{1}')
                two_answer = request.POST.get(f'question_set-{i}-response{2}')
                two_correct = request.POST.get(f'question_set-{i}-correct{2}')
                three_answer = request.POST.get(f'question_set-{i}-response{3}')
                three_correct = request.POST.get(f'question_set-{i}-correct{3}')
                four_answer = request.POST.get(f'question_set-{i}-response{4}')
                four_correct = request.POST.get(f'question_set-{i}-correct{4}')
                questions.append(models.Question(
                    quiz=quiz, 
                    title_anwers=title_anwers, 
                    response1=one_answer,
                    correct1=bool(one_correct),
                    response2=two_answer,
                    correct2=bool(two_correct),
                    response3=three_answer,
                    correct3=bool(three_correct),
                    response4=four_answer,
                    correct4=bool(four_correct),
                ))
            models.Question.objects.bulk_create(questions)
            return redirect(reverse('index'))
    else:
        form = CreateTestForm()
        formset = QuizCreateFormSet()
    return render(
        request, 
        "createtest.html", 
        {
            'form': form,
            'formset': formset 
        }
    )

class ProfileUserView(DetailView):
    model = MyUser
    template_name = 'profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'



class ProfileUserUpdateView(UpdateView):
    model = UserProfile
    template_name = 'profile_update.html'
    slug_url_kwarg = 'user__username'
    slug_field = 'user__username'
    form_class = ProfileUserForm

    def get_success_url(self):
        user = self.request.user
        return reverse('profile', kwargs={'username': user.username})

class ListTestDetailView(DetailView):
    model = Quiz
    template_name = 'test.html'
    slug_url_kwarg = 'title'
    slug_field = 'title'



@login_required
def quiz_detail_passing(request, **kwargs):
    slug_field = kwargs["quiz__title"]
    quiz = get_object_or_404(Quiz, title=slug_field)
    if quiz.quiz_takers.filter(user=request.user).exists():
        return redirect(reverse('index'))
    questions = quiz.question_set.all()
    if request.method == 'POST':
        formset = AnswerFormSet(request.POST)
        
        answers = []
        score = 0
        score_percent = 0
        for i in range(5):
            one_correct = bool(request.POST.get(f'form-{i}-correct1'))
            two_correct = bool(request.POST.get(f'form-{i}-correct2'))
            three_correct = bool(request.POST.get(f'form-{i}-correct3'))
            four_correct = bool(request.POST.get(f'form-{i}-correct4'))
            check_list = [one_correct, two_correct, three_correct, four_correct]   
            if check_list.count(True) != 1:
                messages.error(request,  'Ты быканул?')
                return redirect(reverse('test_passing', args=(slug_field, )))       
            answers.append(
                Answer(
                    question=questions[i],
                    correct1=one_correct, 
                    correct2=two_correct,  
                    correct3=three_correct,
                    correct4=four_correct, 
                )
            )
            if questions[i].correct1 == one_correct \
            and questions[i].correct2 == two_correct \
            and questions[i].correct3 == three_correct \
            and questions[i].correct4 == four_correct:
                score += 1
                score_percent += 1
        models.QuizTakers.objects.create(
            user=request.user,
            quiz=quiz,
            correct_answers=score,
            correct_answers_percent=score_percent*100/5,
        )

        models.Answer.objects.bulk_create(answers)
        return redirect(reverse('result', args=(slug_field, )))
    else:
        formset = AnswerFormSet()
    return render(request, "test_passing.html", {"quiz": quiz, 'formset':formset})



class ListTestView(ListView):
    model = Quiz
    template_name = 'test_all.html'
    context_object_name = 'test'
    extra_context = {'ordering_data': OrderingQuizGetForm, 'filter_passing':OrderingQuizPassing}

    def get_queryset(self):
        if 'ordering_data' in self.request.GET:
            return Quiz.objects.order_by('-created_at')
        if 'filter_passing' in self.request.GET:
            return Quiz.objects.filter(quiz_takers__isnull=False)
        return Quiz.objects.order_by('created_at')

class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comment_create.html'
    form_class = CommentCreateForm

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        pk = self.kwargs['pk']
        quiz = Quiz.objects.get(id=pk)
        object.quiz = quiz
        object.save()
        return super().form_valid(form=form)

    def get_success_url(self):
        titles = self.object.quiz.title
        return reverse('test', kwargs={'title': titles})

class SearchResultsView(ListView):
    model = Quiz
    template_name = 'search_results.html'
    context_object_name = 'test'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Quiz.objects.filter(
            title__icontains=query
        )
        return object_list


class ResultQuiz(DetailView):
    model = QuizTakers
    template_name = 'result.html'
    slug_url_kwarg = 'quiz__title'
    slug_field = 'quiz__title'

    def get_object(self, queryset=None):
        slug = self.kwargs["quiz__title"]
        quiz = get_object_or_404(Quiz, title=slug)
        obj = models.QuizTakers.objects.get(user=self.request.user, quiz=quiz)
        return obj
# def quiz_detail_passing(request, **kwargs):


#     QuizForm = inlineformset_factory(
#         models.Quiz, models.Question, fields=('title',), extra=5
#         )

#     slug_field = kwargs["title"]
#     data = get_object_or_404(Quiz, title=slug_field)
#     if request.method == 'POST':
#         formset = QuizForm(request.POST, request.FIELDS)
#         if formset.is_valid():
#             pass
#     else:
#         formset = QuizForm()
#     return render(request, "test.html", {"quiz": data, 'formset':formset})