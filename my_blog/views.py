from django.shortcuts import render,redirect, get_object_or_404
from . import models
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,logout,login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.   

def PostListView(request):
    categoryQ = request.GET.get('category')
    tagQ = request.GET.get('tag')
    searchQ = request.GET.get('search')
    
    posts = models.Post.objects.all().order_by('-created_at')

    if categoryQ :
        posts = models.Post.objects.filter(category__name__icontains = categoryQ)
    if tagQ :
        posts = models.Post.objects.filter(tag__name__icontains = tagQ)
        if searchQ:
            posts = models.Post.filter(
                Q(title__icontains = searchQ) |
                Q(content__icontains = searchQ) |
                Q(author__username__icontains = searchQ)|
                Q(category__name__icontains = searchQ) |
                Q(tag__name__icontains = searchQ)

            ).distinct()
    paginator = Paginator(posts,2) # Show 2 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj,
        'categoryQ': categoryQ,
        'tagQ': tagQ,
        'searchQ': searchQ,
        'page_obj': page_obj,
        'paginator': paginator,
        'categories': models.Category.objects.all(),
        'tags': models.Tag.objects.all(),
    }
    return render(request,'post_list.html',context)