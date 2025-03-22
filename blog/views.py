from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import json
from django.views.decorators.http import require_POST
from django.conf import settings
import os
import uuid
from gtts import gTTS
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import re

from .models import Post, Comment, Category, Profile
from .forms import (
    PostForm, 
    CommentForm, 
    SignUpForm, 
    ProfileUpdateForm, 
    UserUpdateForm, 
    CategoryForm
)

# Home view
class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# Post detail view
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

# Create post view
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

# Update post view
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete post view
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# User registration view
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Get profile picture and bio from form
            profile_pic = form.cleaned_data.get('profile_pic')
            bio = form.cleaned_data.get('bio')
            # Update user profile
            profile = Profile.objects.get(user=user)
            if profile_pic:
                profile.profile_pic = profile_pic
            if bio:
                profile.bio = bio
            profile.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'blog/register.html', {'form': form})

# User profile view
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_on')
    
    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'posts': posts
    })

# Update profile view
@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        # Create profile if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'blog/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Add comment view
@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', slug=post.slug)
    
    return redirect('post_detail', slug=post.slug)

# Like post view
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

# Category posts view
def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category).order_by('-created_on')
    
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts
    })

# Search view
def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.none()
    
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'query': query
    })

# PDF download view
def download_post_pdf(request, slug):
    post = get_object_or_404(Post, slug=slug)
    template = get_template('blog/pdf_template.html')
    html_string = template.render({'post': post})
    
    # Create a PDF file
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
    
    if not pdf.err:
        # Create HTTP response with PDF
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"{post.slug}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    # If error creating PDF, return error response
    return HttpResponse('Error generating PDF', status=400)

# Generate audio for a post
def generate_post_audio(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Check if audio already exists
    if post.audio_file and os.path.exists(os.path.join(settings.MEDIA_ROOT, post.audio_file.name)):
        # Return the existing audio file URL
        return JsonResponse({'audio_url': post.audio_file.url})
    
    # Clean the text (remove HTML tags)
    content = re.sub('<.*?>', '', post.content)
    
    # Generate audio file using gTTS
    tts = gTTS(text=content, lang='en', slow=False)
    
    # Create a unique filename
    filename = f"post_audio_{uuid.uuid4()}.mp3"
    file_path = os.path.join('post_audio', filename)
    
    # Save the audio file to a temporary file, then to the media storage
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        tts.save(temp_file.name)
        temp_file.flush()
        
        # Save to the post model
        with open(temp_file.name, 'rb') as f:
            post.audio_file.save(file_path, ContentFile(f.read()))
    
    # Delete the temporary file
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)
    
    # Return the audio file URL
    return JsonResponse({'audio_url': post.audio_file.url})
