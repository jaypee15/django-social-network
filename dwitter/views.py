from django.shortcuts import render, redirect
# from django.contrib import messages
from .models import Profile, Post
from .forms import PostForm

def home(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # messages.success(request, 'Your Post was created succesfully')
            return redirect('home')
    followed_posts = Post.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by('-created_at')

    context ={
        'form': form,
        'posts': followed_posts
    }
    # messages.error(request, 'correct the following errors')
    return render(request, 'dwitter/home.html', context)

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'dwitter/profile_list.html', {'profiles': profiles})

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(request.user)
        missing_profile.save()
    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})
    