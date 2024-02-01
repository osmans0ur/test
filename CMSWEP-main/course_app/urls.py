from django.urls import path, include
from .views import (
    courses_page, topics_page, youtube_results_page,
    sign_up, sign_in, sign_out, home, settings, change_password, custom_password_reset,
    quiz_display, quiz_submit, discussion_page, discussion_detail, start_topic, add_comment
)
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path('courses/', courses_page, name='courses_page'),
    path('topics/<int:course_id>/', topics_page, name='topics_page'),
    path('youtube_results/<int:topic_id>/', youtube_results_page, name='youtube_results_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_out/', sign_out, name='logout'),
    path('settings/', settings, name='settings'),
    path('change_password/', change_password, name='change_password'),
    path('forgot_password/', custom_password_reset, name='forgot_password'),
    path('quiz/<int:quiz_id>/', quiz_display, name='quiz_display'),
    path('quiz/<int:quiz_id>/submit/', quiz_submit, name='quiz_submit'),
    path('discussions/', discussion_page, name='discussion_page'),
    path('discussion/<int:discussion_id>/', discussion_detail, name='discussion_detail'),
    path('start_topic/', start_topic, name='start_topic'),
    path('add_comment/<int:discussion_id>/', add_comment, name='add_comment'),
    path('home/', home, name='home'),
]
