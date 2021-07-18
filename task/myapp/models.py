from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms.widgets import DateInput
from task import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from datetime import datetime


class MyUser(AbstractUser):
    username = models.CharField(max_length=24, unique=True)
    
    
    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profiles.save()


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profiles',
        unique=True

    )
    surname = models.CharField(max_length=32)
    yourself_information = models.TextField(default="sest empty")
    photo = models.ImageField(
        default="C:/Users/Denys/Desktop/work/task/media/avatar.png",
        null=True,
        blank=True
    )
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user} |  surname: {self.surname} | yourself_information: {self.yourself_information} | data: {self.date}'
    


class Quiz(models.Model):

    title = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=100)
    created_at = models.DateField(auto_now=True, blank=True)

    class Meta:
        verbose_name_plural ='Quizzes'
    
    def __str__(self):
        return f' {self.title} | {self.description}'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title_anwers = models.CharField(max_length=60)
    response1 = models.CharField(max_length=60)
    correct1 = models.BooleanField(default=False)
    response2 = models.CharField(max_length=60)
    correct2 = models.BooleanField(default=False)
    response3 = models.CharField(max_length=60)
    correct3 = models.BooleanField(default=False)
    response4 = models.CharField(max_length=60)
    correct4 = models.BooleanField(default=False)

    def __str__(self):
        return  f'{self.quiz} | {self.title_anwers} | {self.response1} | {self.response2} | {self.response3} | {self.response4} '


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct1 = models.BooleanField(default=False)
    correct2 = models.BooleanField(default=False)
    correct3 = models.BooleanField(default=False)
    correct4 = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.question}'


class QuizTakers(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='quiz_user_takers')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_takers')
    correct_answers = models.CharField(max_length=4)
    correct_answers_percent = models.IntegerField()

    def __str__(self):
        return self.user.username


class Response(models.Model):
    quiztaker = models.ForeignKey(QuizTakers, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.question

class Comment(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='comments'
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='comment_quiz'
    )
    content = models.TextField()

    def __str__(self):
        return f'{self.user} | {self.content} | {self.quiz}'
