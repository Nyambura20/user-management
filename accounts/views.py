from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
import uuid
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import EditProfile
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.verification_token = str(uuid.uuid4())
            user.is_verified = False
            user.save()
            verification_link = request.build_absolute_uri(
                f"/accounts/verify/{user.verification_token}/"
            )
            # Send real email
            send_mail(
                'Verify your account',
                f'Click the link to verify your account: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, f"Welcome {user.username}! Please check your email to verify your account.")
            return redirect('home')
        else:
            messages.error(request, "There was an error with your form.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_account(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.is_verified = True
        user.verification_token = ''
        user.save()
        messages.success(request, "Your account has been verified! You can now log in.")
        return redirect('login')
    except CustomUser.DoesNotExist:
        return HttpResponse("Invalid verification link.", status=400)
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = EditProfile(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_verified:
            messages.error(self.request, "Please verify your email before logging in.")
            return redirect('login')
        return super().form_valid(form)