from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')  # Or wherever your login URL name is
        else:
            messages.error(request, "There was an error with your form.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
