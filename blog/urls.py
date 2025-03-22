from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Post URLs
    path('', views.HomeView.as_view(), name='home'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    path('post/<slug:slug>/pdf/', views.download_post_pdf, name='download_post_pdf'),
    path('post/<slug:slug>/audio/', views.generate_post_audio, name='generate_post_audio'),
    
    # Category URLs
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    
    # User Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # User Profile URLs
    path('profile/edit/', views.update_profile, name='update_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # Search URL
    path('search/', views.search_posts, name='search_posts'),
]
