# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.username

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    youtube_topic_query = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.course.name} - {self.name}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.topic.course.name} - {self.quiz.topic.name} - {self.quiz.title} - {self.score}"

class Quiz(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.topic.course.name} - {self.topic.name} - {self.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.quiz.topic.course.name} - {self.quiz.topic.name} - {self.quiz.title} - {self.text}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.quiz.topic.course.name} - {self.question.quiz.topic.name} - {self.question.quiz.title} - {self.question.text} - {self.text}"

class Discussion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.author.username}"

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='discussion_files/', null=True, blank=True)

    def __str__(self):
        return f"{self.content[:20]} - {self.author.username} - {self.created_at}"
