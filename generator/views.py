from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import AsciiArt
from .utils import transform_to_ascii
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

# --------------------------------------------------------------------------
# 1. MAIN GENERATOR VIEW
# --------------------------------------------------------------------------
@login_required
def index(request):
    ascii_art = None
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]
        ascii_art = transform_to_ascii(image_file)

    return render(request, "ascii_gen/index.html", {"ascii_art": ascii_art})

# --------------------------------------------------------------------------
# 2. USER HISTORY (PRIVATE)
# --------------------------------------------------------------------------
@login_required
def history_view(request):
    user_art = AsciiArt.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate stats
    public_count = user_art.filter(is_public=True).count()
    private_count = user_art.filter(is_public=False).count()
    
    # Get oldest creation date
    oldest_date = user_art.last().created_at if user_art.exists() else timezone.now()
    
    context = {
        'user_art': user_art,
        'public_count': public_count,
        'private_count': private_count,
        'oldest_date': oldest_date,
    }
    
    return render(request, 'ascii_gen/history.html', context)
# --------------------------------------------------------------------------
# 3. PUBLIC FEED (THE "INSTAGRAM" GALLERY)
# --------------------------------------------------------------------------
def gallery_view(request):
    feed = AsciiArt.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'ascii_gen/gallery.html', {'feed': feed})

# --------------------------------------------------------------------------
# 4. SAVE LOGIC
# --------------------------------------------------------------------------
@login_required
def save_ascii(request):
    if request.method == "POST":
        title = request.POST.get("title")
        ascii_data = request.POST.get("ascii_data")
        is_public = request.POST.get("make_public") == "on"
        
        if ascii_data:
            AsciiArt.objects.create(
                user=request.user,
                title=title if title else "UNTITLED_GEN",
                ascii_text=ascii_data,
                is_public=is_public
            )
            return redirect('save_confirm')
            
    return redirect('index')

# Save confirmation view
@login_required
def save_confirm_view(request):
    return render(request, 'ascii_gen/save_confirm.html')

# --------------------------------------------------------------------------
# 5. AUTHENTICATION: REGISTER
# --------------------------------------------------------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        pc = request.POST.get('password_confirm')

        # Validation Logic
        if not all([u, e, p, pc]):
            messages.error(request, "MISSING_FIELDS")
        elif p != pc:
            messages.error(request, "KEYS_DO_NOT_MATCH")
        elif User.objects.filter(username=u).exists():
            messages.error(request, "HANDLE_ALREADY_TAKEN")
        elif User.objects.filter(email=e).exists():
            messages.error(request, "EMAIL_ALREADY_REGISTERED")
        elif len(p) < 8:
            messages.error(request, "PASSKEY_TOO_SHORT_MIN_8")
        else:
            # Create user
            user = User.objects.create_user(username=u, email=e, password=p)
            
            # FIX: Set the backend on the user object before login
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            # Login the user
            login(request, user)
            messages.success(request, f"IDENTITY_CREATED: {u}")
            return redirect('index')

    return render(request, 'registration/register.html')

# --------------------------------------------------------------------------
# 6. LOGIN VIEW
# --------------------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "INVALID_CREDENTIALS")
    
    return render(request, 'registration/login.html')

# --------------------------------------------------------------------------
# 7. LOGOUT VIEW
# --------------------------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('index')

# --------------------------------------------------------------------------
# 8. DELETE ART
# --------------------------------------------------------------------------
@login_required
def delete_art(request, art_id):
    if request.method == 'POST':
        art = get_object_or_404(AsciiArt, id=art_id, user=request.user)
        art.delete()
        messages.success(request, "ART_DELETED_SUCCESSFULLY")
    return redirect('history')

# --------------------------------------------------------------------------
# ACCOUNT VIEWS
# --------------------------------------------------------------------------

@login_required
def account_view(request):
    # Calculate statistics
    user_art = AsciiArt.objects.filter(user=request.user)
    art_count = user_art.count()
    public_count = user_art.filter(is_public=True).count()
    
    # Calculate days since joining
    join_days = (timezone.now() - request.user.date_joined).days
    
    # Calculate storage used (approximate)
    storage_used = art_count * 0.5  # Approximate KB per ASCII art
    
    context = {
        'art_count': art_count,
        'public_count': public_count,
        'join_days': join_days,
        'storage_used': round(storage_used, 2),
        'last_login': request.user.last_login if request.user.last_login else timezone.now(),
    }
    
    return render(request, 'ascii_gen/account.html', context)

@login_required
def change_username_view(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        password = request.POST.get('password')
        
        # Verify password
        user = authenticate(username=request.user.username, password=password)
        
        if user:
            # Check if username is available
            if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                messages.error(request, 'USERNAME_ALREADY_TAKEN')
            else:
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'USERNAME_UPDATED_SUCCESSFULLY')
                update_session_auth_hash(request, request.user)
        else:
            messages.error(request, 'INVALID_PASSWORD')
    
    return redirect('account')

@login_required
def change_email_view(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        password = request.POST.get('password')
        
        # Verify password
        user = authenticate(username=request.user.username, password=password)
        
        if user:
            # Check if email is available
            if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
                messages.error(request, 'EMAIL_ALREADY_REGISTERED')
            else:
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'EMAIL_UPDATED_SUCCESSFULLY')
        else:
            messages.error(request, 'INVALID_PASSWORD')
    
    return redirect('account')

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'PASSWORD_UPDATED_SUCCESSFULLY')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return redirect('account')

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Verify password
        user = authenticate(username=request.user.username, password=password)
        
        if user:
            # Delete all user's ASCII art
            AsciiArt.objects.filter(user=user).delete()
            
            # Delete user account
            user.delete()
            
            # Logout
            logout(request)
            
            messages.success(request, 'ACCOUNT_DELETED_SUCCESSFULLY')
            return redirect('index')
        else:
            messages.error(request, 'INVALID_PASSWORD')
    
    return redirect('account')

def verify_request_view(request):
    # This is a placeholder for email verification
    if request.user.is_authenticated:
        messages.info(request, 'VERIFICATION_EMAIL_SENT')
        # In a real app, you would send an email verification link here
    return redirect('account')

# --------------------------------------------------------------------------
# INFO PAGES
# --------------------------------------------------------------------------

def about_view(request):
    return render(request, 'ascii_gen/about.html')

def privacy_view(request):
    return render(request, 'ascii_gen/privacy.html')

def terms_view(request):
    return render(request, 'ascii_gen/terms.html')