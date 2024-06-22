"""
URL configuration for MelkamEjoch project.

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
from website.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('profile/update/',profile_update, name='profile_update'),
    path('profile/delete/', profile_delete_confirm, name='profile_delete_confirm'),
    path('profile/delete/confirmed/', profile_delete, name='profile_delete'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='Home'),
    path('charity/', charities, name='charity'),
    path('charity/<int:id>/', charity_detail, name='charity-detail'),
    path('projects/', project_list, name='project-list'),
    path('make_donation/<int:user_id>/<int:project_id>/<int:charity_id>/', make_donation, name='make_donation'),
    path('user_donations/', user_donations, name='donations'),
    path('download_receipt/<int:donation_id>/', download_receipt, name='download_receipt'),
    path('add_charity/', add_charity_view, name='add_charity'),
    path('new_charity/', new_charity, name='new_charity'),
    path('set_charity_status/<int:charity_id>/',set_charity_status, name='set_charity_status'),
    path('remove_charity/<int:charity_id>/', remove_charity, name='remove_charity'),
    path('add-project/', add_project, name='add_project'),
    path('new_project/', new_project, name='new_project'),
    path('remove_project/<int:project_id>/', remove_project, name='remove_project'),
    path('set_project_status/<int:project_id>/', set_project_status, name='set_project_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

