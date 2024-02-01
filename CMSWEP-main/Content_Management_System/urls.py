# myproject/urls.py
from django.contrib import admin
from django.urls import include, path
from course_app.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
     path('', home, name='home'),
    path('course_app/', include('course_app.urls')),
]
