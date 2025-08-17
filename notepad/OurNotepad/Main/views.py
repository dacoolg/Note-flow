from django.contrib.auth.decorators import login_required
from .models import Note
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteForm, SearchForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
# Create your views here.

def HomePage(request):
    """
    Render the home page of the application.
    """
    return render(request, "homepage.html")

@login_required(login_url='login')
def NotesList(request):
    notes = Note.objects.filter(owner=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            notes = Note.objects.filter(owner=request.user, title__icontains=query) | \
                    Note.objects.filter(owner=request.user, content__icontains=query)
    else:
        form = SearchForm()
    return render(request, 'note-recent.html', {'notes': notes, 'form': form})

@login_required(login_url='login')
def CreateNote(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            try:
                note = form.save(commit=False)
                note.owner = request.user
                note.save()
                return redirect('recent-notes')
            except IntegrityError:
                form.add_error(None, "A note with this title already exists. Please use a different title.")
    else:
        form = NoteForm()
    return render(request, 'notes-create.html', {'form': form})

@login_required(login_url='login')
def NoteDetail(request, slug):
    note = get_object_or_404(Note, slug=slug, owner=request.user)
    return render(request, 'note-detail.html', {'note': note})

@login_required(login_url='login')
def edit_note(request,slug):
    note = get_object_or_404(Note, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note-detail', slug=note.slug)
    else:
        form = NoteForm(instance=note)
    
    return render(request, 'note-edit.html', {'form': form, 'note': note})


@login_required(login_url='login')
def delete_note(request, slug):
    note = get_object_or_404(Note, slug=slug, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('recent-notes')
    return render(request, 'note-delete.html', {'note': note})

@login_required(login_url='login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep session alive
            return redirect('recent-notes')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'notes-account-password-change.html', {'form': form})

@login_required(login_url='login')
def account(request):
    return render(request, 'notes-account.html')

def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recent-notes')
    return render(request, "notes-signup.html", {'form': form})

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('recent-notes')
    return render(request, "notes-login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')