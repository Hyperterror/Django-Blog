from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,User,Category,Tag
from django.utils import timezone
from .forms import PostForm, UserForm, LoginForm, ProfileForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def post_list(request):
  post=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
  return render(request,'blog/post_list.html',{'posts':post})


@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    tags=post.tag.all()
    cats=Category.objects.all()
    Tags=Tag.objects.all()

    return render(request, 'blog/post_detail.html', {'post': post,'tags':tags,'all_tag':Tags,'cats':cats})
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
#need to add a condition as any user can change any post right now
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def sign_up(request):
    form=UserForm()
    context={'form':form}
    if request.method=='POST':
        first_name= request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        city=request.POST.get("city")
        state=request.POST.get("state")
        image=request.FILES.get("image")
        phone_number=request.POST.get("phone_no")

        user=User.objects.filter(email=email)

        if user.exists():
            messages.info(request, "Email already Used")
            return redirect('login')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password, 
            first_name=first_name,
            last_name=last_name,
            city=city,
            state=state,
            image=image,
            phone_number=phone_number,
        )

        messages.info(request, "Sign Up Successful")
        return redirect('login')

    return render(request,'blog/signup.html',context)

def login_view(request):
    form=LoginForm()
    context={'form':form}
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect('login')

        auth_login(request, user)
        return redirect('post_list')
    return render(request,'blog/login.html',context)


@login_required
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-published_date')
    return render(request, 'blog/profile.html', {'user': user, 'posts': posts})
    

def logout_view(request):
    if request.method=='POST':
        logout(request)
        return redirect('login')
    return render(request,'blog/logout.html')


@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'blog/profile_edit.html', {'form': form})


def category_view(request,slug):
    cat=get_object_or_404(Category,slug=slug)
    post=Post.objects.filter(category=cat).order_by('published_date')
    return render(request,'blog/category.html',{'posts':post,'cat':cat})


def tag_view(request,slug):
    tags=get_object_or_404(Tag,slug=slug)
    post=Post.objects.filter(tag=tags).order_by("published_date")

    return render(request,'blog/tags.html',{'posts':post,'tag':tags})
