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
    AnswerFormSet
)
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.db.models import Avg, Q
from django.forms.models import inlineformset_factory
from django.forms import formset_factory
import operator

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


# class CreateTestView(CreateView):
#     model = Quiz
#     form_class = CreateTestForm
#     template_name = 'createtest.html'
#     success_url = reverse_lazy('index')

#     def form_valid(self, form):
#         object = form.save(commit=False)
#         object.user = self.request.user
#         return super().form_valid(form=form)

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
    # if request.method == 'POST':
    #     # import pdb
    #     # pdb.set_trace()
    #     title = request.POST.get('title')
    #     description = request.POST.get('description')
    #     form = CreateTestForm({'title': title, 'description': description})
    #     if form.is_valid():
    #         quiz = form.save()
    #         questions = []
    #         for i in range(5):
    #             title_question = request.POST.get(f'question_set-{i}-title_question')
    #             questions.append(models.Question(quiz=quiz, title_question=title_question))
    #             one_answer = request.POST.get('answer_set-0-text')[i]
    #             two_answer = request.POST.get('answer_set-1-text')[i]
    #             three_answer = request.POST.get('answer_set-2-text')[i]
    #             four_answer = request.POST.get('answer_set-3-text')[i]
    #         models.Question.objects.bulk_create(questions)
    #     test_formset_title = test_formset_title(request.POST)
    #     formset = test_formset(request.POST)
    #     form = CreateTestForm(request.POST)
    #     if form.is_valid() and test_formset_title.is_valid() and formset.is_valid():
    #         pass
    # else:
    #     test_formset_title = test_formset_title()
    #     formset = test_formset()
    #     form = CreateTestForm()
    # return render(
    #     request, 
    #     "createtest.html", 
    #     {'form': form, 
    #     'formset': formset ,
    #     }
    # )
class ProfileUserView(DetailView):
    model = MyUser
    template_name = 'profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     obj = kwargs['object']
    #     context.update({'profile_form': ProfileUserForm(instance=obj)})
    #     return context

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


# answer_formset = inlineformset_factory(
#         models.Question,
#         models.Answer,
#         fields=(
#             'correct1', 
#             'correct2',
#             'correct3',
#             'correct4',
#         ),
#         extra=5,
#         can_delete=False,
# )


def quiz_detail_passing(request, **kwargs):
    slug_field = kwargs["title"]
    data = get_object_or_404(Quiz, title=slug_field)
    questions = data.question_set.all()
    if request.method == 'POST':
        # formset = AnswerFormSet(request.POST, request.FIELDS)
        
        answers = []
        for i in range(5):
            one_correct = request.POST.get(f'form-{i}-correct1')
            two_correct = request.POST.get(f'form-{i}-correct2')
            three_correct = request.POST.get(f'form-{i}-correct3')
            four_correct = request.POST.get(f'form-{i}-correct4')
            my_one_correct = request.POST.get(f'form-{i}-correct1')
            answers.append(
                Answer(
                    question=questions[i],
                    correct1=bool(one_correct), 
                    correct2=bool(two_correct),  
                    correct3=bool(three_correct),
                    correct4=bool(four_correct) 
                )
            )
        # breakpoint()

        question = models.Question.objects.get(title=data).values(
            'correct1', 
            'correct2', 
            'correct3', 
            'correct4'
        )
        if answers == question:
            return True
        if formset.is_valid():
            pass
    else:
        formset = AnswerFormSet()
    return render(request, "test_passing.html", {"quiz": data, 'formset':formset})



    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if 'title' in self.kwargs:
    #         title = self.kwargs['title']
    #         quiz = models.Quiz.objects.get(title=title)
    #         context['quiz'] = quiz
    #     return context






# def quiz_detail_passing(request, **kwargs):

#     QuizForm = inlineformset_factory(
#         models.Quiz, models.Question, fields=('title_question',), extra=5
#         )

#     slug_field = kwargs["title"]
#     data = get_object_or_404(Quiz, title=slug_field)
#     if request.method == 'POST':
#         formset = QuizForm(request.POST, request.FIELDS)
#         if formset.is_valid():
#             pass
#     else:
#         formset = QuizForm()
#     return render(request, "test_passing.html", {"quiz": data, 'formset':formset})

class ListTestView(ListView):
    model = Quiz
    template_name = 'test_all.html'
    context_object_name = 'test'
    extra_context = {'ordering_data': OrderingQuizGetForm}

    def get_queryset(self):
        if 'ordering_data' in self.request.GET:
            return Quiz.objects.order_by('-created_at')
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
            Q(title__icontains=query)
        )
        return object_list

class ResultQuiz(DetailView):
    model = Quiz
    template_name = 'result.html'
    slug_url_kwarg = 'title'
    slug_field = 'title'


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