from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Post,UserProfile
from .forms import CustomUserCreationForm, PostForm, LoginForm
from django.http import  HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, authenticate
import logging
from ipware import get_client_ip

def ip_address(request):
    x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forward:
        ip = x_forward.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def posts (request):
    response = []
    posts = Post.objects.filter().order_by('-datetime')
    for post in posts:
        response.append(
            {
                'datetime': post.datetime,
                'content' :  post.content,
                'author': f"{post.user.first_name} {post.user.last_name}",
                'hash': post.hash,
                'txId': post.txId
            }
        )

    return JsonResponse(response, safe=False)

def wordCheck(request):
    word = request.GET.get('', 'btc')
    posts = Post.objects.filter()
    count = 0
    x = str(word)
    for post in posts:
        if x in post.content:
            count += 1
    return HttpResponse(f'La parola {x} è stata scritta {count} volte nei post')

def newPost(request):
    this_ip = ip_address(request)
    user = request.user
    if not user.is_superuser:
        prof_user = user.username

        x = UserProfile.objects.filter(username=prof_user).values('ipAddress')

        if this_ip != x:
            messages.info(request, 'Attenzione! indirizzo IP differente!')
            UserProfile.objects.filter(username=prof_user).update(ipAddress=this_ip)

    posts = Post.objects.order_by('datetime')
    return render(request, 'blog/newPost.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            ip = ip_address(request)
            print(ip)
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

    else:
        f = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': f})

def posting(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post=form.save()
            return redirect('newPost')
    else:
        form = PostForm()
    return render(request, 'blog/posting.html', {'form': form})

logger = logging.getLogger('textlogger')

def login(request):
    ip = get_client_ip(request)
    print('ip: ', ip)
    next = request.GET.get('next')
    title = 'Login'
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username');
        password = form.cleaned_data.get('password');
        user = authenticate(username=username, password=password)
        logger.info(''.join([ip_address, ' logged in']))
        login(request, user)
        if next:
            return redirect(next)
        return redirect('newPost')


    return render(request, 'login.html', {'form': form, 'ip': ip})


def counter(request):
    user_list = User.objects.filter(is_superuser=False)
    total_post = {}
    for user in user_list:
        count = 0
        posts = Post.objects.filter(user=user).values()
        for post in posts:
            count += 1
        total_post[user.username] = count

    return render(request, 'blog/counter.html', {'total_post': total_post})

def id_user(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render (request, 'blog/id_user.html', context)

def lastPosts(request):
    l_posts = []
    now = timezone.now()
    posts = Post.objects.filter().order_by('-datetime')
    for post in posts:
        if now - post.datetime <= timedelta(0, 5444):
            l_posts.append(
                {
                    'author': f"{ post.user }",
                    'content': post.content,
                    'datetime': post.datetime
                }
            )
    return JsonResponse(l_posts, safe=False)