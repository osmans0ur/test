from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from .models import Course, Topic, CustomUser, Quiz, Answer, Discussion, Comment
from .forms import SignUpForm, SignInForm, UserUpdateForm, DiscussionForm, CommentForm, YourForm
import requests
from django.utils.decorators import method_decorator
from django.views import View


def home(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'registration/sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('home')


@login_required
def settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'settings.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('settings')
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {
        'password_change_form': password_change_form,
    })


def custom_password_reset(request):
    return PasswordResetView.as_view(
        request,
        template_name='forgot_password.html',
        email_template_name='forgot_password_email.html',
        subject_template_name='forgot_password_subject.txt',
        post_reset_redirect='/course_app/sign_in/',
    )


def courses_page(request):
    courses = Course.objects.all()
    return render(request, 'course_app/courses_page.html', {'courses': courses})


def topics_page(request, course_id):
    course = Course.objects.get(pk=course_id)
    topics = Topic.objects.filter(course=course)
    return render(request, 'course_app/topics_page.html', {'course': course, 'topics': topics})


def youtube_results_page(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    youtube_api_key = 'your_youtube_api_key'
    youtube_query = topic.youtube_topic_query

    response = requests.get(f'https://www.googleapis.com/youtube/v3/search?q={youtube_query}&key={youtube_api_key}')
    data = response.json()
    videos = data.get('items', [])

    return render(request, 'course_app/youtube_results_page.html', {'topic': topic, 'videos': videos})


def quiz_display(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    return render(request, 'course_app/quiz_display.html', {'quiz': quiz})


def quiz_submit(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(pk=quiz_id)
        score = 0

        for question in quiz.question_set.all():
            selected_answer_id = request.POST.get(f'question_{question.id}')

            if selected_answer_id:
                selected_answer = Answer.objects.get(pk=selected_answer_id)

                if selected_answer.is_correct:
                    score += 1

        return render(request, 'course_app/quiz_result.html', {'quiz': quiz, 'score': score})

    return redirect('home')


@login_required
def discussion_page(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            content = form.cleaned_data['content']
            Discussion.objects.create(topic=topic, content=content)
            return redirect('discussions_list')
    else:
        form = YourForm()

    discussions = Discussion.objects.all()
    return render(request, 'discussions/discussions_list.html', {'discussions': discussions, 'form': form})


@login_required
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    comments = discussion.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.discussion = discussion
            new_comment.author = request.user
            new_comment.save()
            return redirect('discussion_detail', discussion_id=discussion.id)
    else:
        form = CommentForm()

    return render(request, 'discussions/discussion_detail.html', {'discussion': discussion, 'comments': comments, 'form': form})


@login_required
def start_topic(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            new_discussion = form.save(commit=False)
            new_discussion.author = request.user
            new_discussion.save()
            return redirect('discussion_detail', discussion_id=new_discussion.id)
    else:
        form = DiscussionForm()

    return render(request, 'discussions/start_topic.html', {'form': form})


def add_comment(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.author = request.user
            comment.save()
            return redirect('discussion_detail', discussion_id=discussion.id)
    else:
        form = CommentForm()

    return render(request, 'discussions/add_comment.html', {'form': form, 'discussion': discussion})
