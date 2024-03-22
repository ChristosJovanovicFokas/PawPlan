"""
URL configuration for pawplan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from core import views
from django.conf.urls.static import static
from core import views
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("animals", views.animal_list, name="animal_list"),
    path("dashboard/", views.worker_dash, name="worker_dash"),
<<<<<<< HEAD
    path("about/", views.about_view, name="about"),
]
=======
    path("", views.home, name="home"),
    path('about/', views.about_view, name='about'),
    path('adopt/', views.adopt, name='adopt'),
    path('login/', views.login, name='login')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 02a38d4cf6bcc6ec72386a337a8e567805eab23d
