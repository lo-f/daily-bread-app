from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.views import LoginView # type: ignore
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class Home(LoginView):
    template_name = 'home.html'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)