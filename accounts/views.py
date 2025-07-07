from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
import uuid
from django.http import HttpResponse
from .models import CustomUser

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
            print(f"Verification link for {user.email}: {verification_link}")
            messages.success(request, "Account created! Please check your email to verify your account.")
            return redirect('login')
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
