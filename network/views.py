from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import constraints
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages # imports messages
import json

from .utilities import get_previous_page, get_next_page
from .models import User, Post
from .forms import NewPostForm

# everyone can see all the posts
def index(request):
    
    posts = Post.objects.all()
    paginator = Paginator(posts, 10) # shows 10 pages per page
    
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    
    return render(request, "network/index.html", {
        'form': NewPostForm(),
        'page': page,
        'previous_page': get_previous_page,
        'next_page': get_next_page
    })

@csrf_exempt
@login_required
def editpost(request, post_id):
    
    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # The user requesting to edit the post must be the author
    if request.user == post.author:
        # Decodes the request to pull out the 'content'
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']
    
    # Updates post with new content    
    Post.objects.filter(pk=post_id).update(content=f'{content}')
    
    # Returns Json Response with content passed back that we can use with JS to update page
    return JsonResponse({"message": "Post updated successfully.", "content": content}, status=200)

@csrf_exempt
@login_required
def updatelike(request, post_id):
    
    # Saves user and post from the request
    user = request.user
    
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."},status=404)

    # If the user has liked the post, unlike it
    if (user.likes.filter(pk=post_id).exists()):
        post.liked_by.remove(user)
        likes_post = False
    # if the user has unliked/doesn't like the post, like it
    else:
        post.liked_by.add(user)
        likes_post = True
    
    # Save updated no. of likes
    likes = post.likes() 
       
    return JsonResponse({"likesPost": likes_post, "likesCount": likes}, status=200)

@login_required
def newpost(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Takes form from POST request
    form = NewPostForm(request.POST)
    
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return HttpResponseRedirect(reverse("index"))
    
def profile(request, user_id):
    
    # Looks up the user's profile page
    profile_user = User.objects.get(pk = user_id)

    # Searches for the user's posts
    profile_posts = Post.objects.filter(author=user_id)
    paginator = Paginator(profile_posts, 10) # shows 10 pages per page on the profile
    
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    # Tells you if logged in user is following this user
    if request.user.is_authenticated:
        following = profile_user.followers.filter(id = request.user.id).exists()
    else:
        following = False
    
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "following": following,
        "followers_count": profile_user.followers.all().count(),
        "following_count": profile_user.following.all().count(),
        'form': NewPostForm(),
        'page': page,
        'previous_page_url': get_previous_page,
        'next_page_url': get_next_page
    })
     
@login_required(login_url='login')
def follow(request, user_to_follow):
    
    # Following a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."},status=400)
    
    # Add 'user_to_follow' to following list of the user
    User.objects.get(pk=request.user.id).following.add(user_to_follow)
    # reloads 'user_to_follow' page
    return HttpResponseRedirect(reverse("profile", args=(user_to_follow,)))

@login_required(login_url='login')
def unfollow(request, user_to_unfollow):
   
    # Unfollowing a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."},status=400)
    
    # removes 'user_to_follow' to following list of the user
    User.objects.get(pk=request.user.id).following.remove(user_to_unfollow)
    # reloads 'user_to_follow' page
    return HttpResponseRedirect(reverse("profile", args=(user_to_unfollow,)))

@login_required(login_url='login')
def following(request):

    # Queries who the user is following
    following = User.objects.get(pk=request.user.id).following.all()
    
    # Creates a list of ids, which we will use in the 'following_posts' query below
    following_ids = following.values_list('pk', flat=True)
    
    # Fiiters to only show the posts from the accounts the user follows
    following_posts = Post.objects.filter(author__in=following_ids)
    
    paginator = Paginator(following_posts, 10)
    
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
       "posts": following_posts,
       'page': page
    }) 
        
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
           messages.error(request, 'Invalid username and/or password.')
           return render(request, "network/login.html")
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, 'Passwords must match.')
            return render(request, "network/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
