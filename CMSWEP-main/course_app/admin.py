from django.contrib import admin
from .models import Course, Topic, CustomUser, Quiz, Question, Answer, Discussion, Comment

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 3

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(CustomUser)
admin.site.register(Discussion)
admin.site.register(Comment)
