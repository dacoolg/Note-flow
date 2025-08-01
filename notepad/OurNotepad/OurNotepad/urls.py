"""
URL configuration for OurNotepad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from Main import views

urlpatterns = [
    path("",views.HomePage,name="home"),
    path('admin/', admin.site.urls),
    path("recent-notes/", views.NotesList, name="recent-notes"),
    path("create-note/", views.CreateNote, name="create-note"),
    path('notes/<slug:slug>/', views.NoteDetail, name='note-detail'),
    path('notes/<slug:slug>/edit/', views.edit_note, name='edit-note'),
    path('notes/<slug:slug>/delete/', views.delete_note, name='delete-note'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('password-change/', views.password_change, name='password-change'),
]
