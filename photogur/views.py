from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from photogur.models import Picture, Comment

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
    search_results = Picture.objects.filter(artist=query)
    context = {
        'pictures': search_results,
        'query': query,
    }
    response = render(request, 'picture_search.html', context)
    return HttpResponse(response)

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
