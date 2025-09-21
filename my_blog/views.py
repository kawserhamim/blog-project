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
        posts = models.Post.objects.filter(
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
    return render(request,'my_blog/post_list.html',context)

def PostDetailView(request,pk):
    post = get_object_or_404(models.Post,pk=pk)
    post.view_count += 1
    post.save()
    
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = forms.CommentForm()

    comments = post.comment_set.all()
    is_liked = post.liked_users.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    like_count = post.liked_users.count()
    liked_users = post.liked_users.all() if is_liked else None

    # comments = models.Comment.objects.filter(post=post)
    # is_liked = False
    # if post.liked_users.filter(id=request.user.id).exists():
    #     is_liked = True         
    context = {
        'post': post,       
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'like_count': like_count,
        'comment_form': form,
        'categories': models.Category.objects.all(),
        'tags' : models.Tag.objects.all(), 
    }
    return render(request,'my_blog/post_detail.html',context)

def LikePost(request,id):
    post = get_object_or_404(models.Post,pk=id)
    if post.liked_users.filter(id=request.user.id).exists():
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)
    return redirect('post_detail',pk=post.pk)

def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('post_detail', pk=post.pk)
    else:
        form = forms.PostForm()
    return render(request, 'my_blog/create_post.html', {'form': form})

def edit_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)
    if request.method == 'POST':
        form = forms.PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = forms.PostForm(instance=post)
    return render(request, 'my_blog/edit_post.html', {'form': form, 'post': post})

def delete_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'my_blog/delete_post.html', {'post': post})\
    

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'my_blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'my_blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('post_list')