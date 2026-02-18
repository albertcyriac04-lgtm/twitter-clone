from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Tweet, Like
from .forms import TweetForm, RegisterForm

def feed(request):
    tweets = Tweet.objects.select_related('author').prefetch_related('likes').all()
    form = TweetForm()

    # Add liked status for each tweet
    tweet_list = []
    for tweet in tweets:
        tweet.is_liked = False
        if request.user.is_authenticated:
            tweet.is_liked = tweet.likes.filter(user=request.user).exists()
        tweet_list.append(tweet)

    return render(request, 'feed.html', {'tweets': tweet_list, 'form': form})

@login_required
@require_POST
def create_tweet(request):
    form = TweetForm(request.POST)
    if form.is_valid():
        tweet = form.save(commit=False)
        tweet.author = request.user
        tweet.save()
    return redirect('feed')

@login_required
@require_POST
def toggle_like(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': tweet.like_count()})

@login_required
@require_POST
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, author=request.user)
    tweet.delete()
    return redirect('feed')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        else:
            error = 'Invalid username or password'
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('feed')
