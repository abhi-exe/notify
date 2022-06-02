from django.forms import PasswordInput
from django.shortcuts import render, get_object_or_404, redirect

from notes.forms import NoteForm, LoginForm, SearchForm
from .models import Note, User
# Create your views here.
isloggedin=0
user=0

def login(request):
    if request.method=="POST":
        form= LoginForm(request.POST)
        if form.is_valid():
            try:
                myuser=User.objects.get(email=request.POST['email'],password=request.POST['password'])
                global user
                user=get_object_or_404(User,pk=myuser.pk)
                global isloggedin
                isloggedin=1
                return redirect('noteshomeroute')
            except User.DoesNotExist:
                return render(request,'notes/login.html',{'form': form,'error': 'Invalid Credentials'})
    else:
        form= LoginForm()
    return render(request,'notes/login.html',{'form': form,'error': ''})

def notelist(request):
    if isloggedin!=1:
        return redirect('loginroute')
    notelist1=Note.objects.filter(author=user)
    return render(request,'notes/noteslist.html',{'notelist': notelist1})

def viewnote(request,pk):
    if isloggedin!=1:
        return redirect('loginroute')
    note=get_object_or_404(Note, pk=pk, author=user)
    return render(request, 'notes/viewnote.html',{'note':note})

def newnote(request):
    if isloggedin!=1:
        return redirect('loginroute')
    if request.method=="POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.savetoapp()
            return redirect('singlenote',pk=post.pk)
    else:
        form = NoteForm()
    return render(request,'notes/editnote.html',{'form': form})

def changenote(request,pk):
    if isloggedin!=1:
        return redirect('loginroute')
    post = get_object_or_404(Note, pk=pk, author=user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.savetoapp()
            return redirect('singlenote', pk=post.pk)
    else:
        form = NoteForm(instance=post)
    return render(request, 'notes/editnote.html', {'form': form})

def signout(request):
    global user
    user=0
    global isloggedin
    isloggedin=0
    return redirect('loginroute')

def signup(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            try:
                myuser=User.objects.get(email=request.POST['email'])
                return render(request,'notes/signup.html',{'form': form,'error': 'Already Exists'})
            except User.DoesNotExist:
                post=form.save()
                return redirect('loginroute')
    else:
        form=LoginForm()
    return render(request,'notes/signup.html',{'form': form,'error': ''})

def deletenote(request,pk):
    if isloggedin!=1:
        return redirect('loginroute')
    note=get_object_or_404(Note, pk=pk, author=user)
    note.delete()
    return redirect('noteshomeroute')

def tagfilter(request):
    if isloggedin!=1:
        return redirect('loginroute')
    if request.method=="POST":
        form=SearchForm(request.POST)
        if form.is_valid():
            tags=request.POST['tags']
            notelist1=Note.objects.filter(tags__contains=tags,author=user)
            return render(request,'notes/tagfilter.html',{'form':form,'notelist': notelist1})

    else:
        form=SearchForm()
    return render(request,'notes/tagfilter.html',{'form':form,'notelist':[]})