# pinkky/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Location
import json
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .models import Location



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import PostForm

@login_required(login_url='login')
def post_create(request):
    location_id = request.session.get('location_id')
    location = None
    if location_id:
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            request.session.pop('location_id', None) 
            location = None

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if location:
                post.location = location            
            post.save()
            request.session.pop('location_id', None)
            
            return redirect('post_list') 
    else:
        form = PostForm()
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'post_create.html', {
        'form': form,
        'posts': posts,
        'location': location,
    })

def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            # Update the location if provided
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                post.location.latitude = latitude
                post.location.longitude = longitude
                post.location.save()
            
            post.save()
            return redirect('post_detail', post_id=post.id)
    
    else:
        form = PostForm(instance=post)

    return render(request, 'post_edit.html', {'form': form, 'post': post})

# ฟังก์ชันลบโพสต์
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')  # เปลี่ยนไปยังหน้ารายการโพสต์
    return render(request, 'post_delete.html', {'post': post})

@login_required
def post_list(request):
    location_id = request.session.get('location_id')
    location = None

    if location_id:
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            request.session.pop('location_id', None)  # Clear invalid session data

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Attach location if it exists in the session
            if location:
                post.location = location
            post.save()

            # Clear the session after saving the post
            request.session.pop('location_id', None)

            return redirect('post_list')

    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'post_list.html', {
        'form': form,
        'posts': posts,
        'location': location,
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    print(post.location.latitude, post.location.longitude)
    return render(request, 'post_detail.html', {'post': post})

def save_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            # Create the location object and save it
            location = Location.objects.create(
                latitude=latitude,
                longitude=longitude
            )
            # Store the location ID in the session
            request.session['location_id'] = location.id

            # Return a success response in JSON format
            return JsonResponse({'success': True, 'location_id': location.id})

    # Return an error response if something went wrong
    return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

def register(req):
    if req.method == 'POST':  # Only process the form if it's a POST request
        username = req.POST['username']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']
        email = req.POST['email']
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']

        # Check if passwords match
        if password != confirm_password:
            messages.error(req, "Passwords do not match.")
        # Check if username already exists
        elif User.objects.filter(username=username).exists():
            messages.error(req, "Username already exists.")
        # Check if email already exists
        elif User.objects.filter(email=email).exists():
            messages.error(req, "Email already exists.")
        else:
            # Create user if validation passes
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            messages.success(req, "User created successfully!")
            login(req, user)
            return redirect('login')  # Redirect to the home page or any other page

    return render(req, 'register.html')



class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('post_list')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

@login_required
def post_list_user(request):
    # กรองโพสต์ตามผู้ใช้ที่ล็อกอินอยู่
    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    # หากเป็นการร้องขอแบบ POST (เช่นการสร้างโพสต์ใหม่)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # ตั้งผู้เขียนเป็นผู้ใช้ที่ล็อกอิน
            post.save()
            return redirect('post_list')  # รีไดเรกไปที่ post_list หลังจากบันทึกโพสต์แล้ว
    else:
        form = PostForm()

    # ส่งข้อมูลโพสต์และฟอร์มไปยัง template
    return render(request, 'post_list_user.html', {
        'form': form,
        'posts': posts,
    })
