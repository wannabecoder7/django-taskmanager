from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to TaskManager API 🚀"})

urlpatterns = [
    path('', home), 
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/tasks/", include("tasks.urls")),
    path("api/notes/", include("notes.urls")),
]
