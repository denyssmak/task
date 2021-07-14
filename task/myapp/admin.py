from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, UserProfile, Quiz, Question, Answer, Response, QuizTakers

import nested_admin

class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4
    max_num = 4
    can_delete = False


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [AnswerInline,]
    extra = 4
    can_delete = False


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline,]


class ResponseInline(admin.TabularInline):
    model = Response


class QuizTakersAdmin(admin.ModelAdmin):
    inlines = [ResponseInline,]
    admin.site.register(Quiz, QuizAdmin)
    admin.site.register(Question)
    admin.site.register(Response)

admin.site.register(MyUser, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Answer)