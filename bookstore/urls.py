
from django.contrib import admin
from django.urls import path, include
from books.views import test_storage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('test-storage/', test_storage),  # dòng test
]