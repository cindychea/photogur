from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from photogur.models import Picture, Comment
from photogur.forms import LoginForm, PictureForm


def root(request):
    return HttpResponseRedirect('pictures')

def pictures(request):
    context = {
        'title': 'Photogur',
        'pictures': Picture.objects.all(),
    }
    response = render(request, 'pictures.html', context) 
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {
        'title': 'Selected Picture',
        'picture': picture
    }
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def picture_search(request):
    query = request.GET['query']
    search_results = (Picture.objects.filter(title__icontains=query)) | Picture.objects.filter(artist__icontains=query)
    context = {
        'pictures': search_results,
        'query': query,
    }
    response = render(request, 'picture_search.html', context)
    return HttpResponse(response)

# combining decorators? e.g. login required
@require_http_methods(['POST'])
def create_comment(request):
    user_name = request.POST['name']
    user_message = request.POST['message']
    picture_id = request.POST['picture']
    picture = Picture.objects.get(id=picture_id)
    # comment = Comment(name=user_name, picture=picture, message=user_message)
    # comment.save()
    Comment.objects.create(name=user_name, picture=picture, message=user_message)
    return redirect('picture_show', id=picture_id)

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
                # why do I have to put /pictures here and not in the def root?
            else: 
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()  
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_pw = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_pw)
            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required
def add_picture(request):
    if request.method == 'POST':
        picture_form = PictureForm(request.POST)
        if picture_form.is_valid():
            new_pic = picture_form.save(commit=False)
            new_pic.user = request.user
            picture_form.save()
            return redirect('/pictures', id=new_pic.id)
    else:
        picture_form = PictureForm()
        return render(request, 'add_picture.html', {'picture_form': picture_form})

@login_required
def edit_picture(request, id):
    picture = get_object_or_404(Picture, id=id, user=request.user.pk)
    print(picture.user)
    if request.method == 'POST':
        picture_form = PictureForm(request.POST, instance=picture)
        if picture_form.is_valid():
            picture_form.save()
            return redirect('/pictures', id=picture.id)
    else:
        picture_form = PictureForm(instance=picture)
        return render(request, 'edit_picture.html', {'picture_form': picture_form, 'picture': picture})
