from . import views
from django.urls import path, include

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('history/', views.history_view, name='history'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('save/', views.save_ascii, name='save_ascii'),
    path('delete/<int:art_id>/', views.delete_art, name='delete_art'),
    path('save/confirm/', views.save_confirm_view, name='save_confirm'),
    
    # Your custom auth URLs (BEFORE allauth)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Allauth for social login only
    path('social/', include('allauth.urls')),  # Changed from 'accounts/' to 'social/'
    
    # Account management URLs
    path('account/', views.account_view, name='account'),
    path('account/change-username/', views.change_username_view, name='change_username'),
    path('account/change-email/', views.change_email_view, name='change_email'),
    path('account/change-password/', views.change_password_view, name='change_password'),
    path('account/delete/', views.delete_account_view, name='delete_account'),
    path('account/verify/', views.verify_request_view, name='verify_request'),
    
    # Info pages
    path('about/', views.about_view, name='about'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
]