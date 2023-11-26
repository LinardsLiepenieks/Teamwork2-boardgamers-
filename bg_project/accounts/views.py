from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from boardgames.models import Boardgame


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('boardgames:index')
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def profile(request):
    context = {}
    context['user'] = request.user
    context['boardgames'] = Boardgame.objects.filter(user=context['user'])
    return render(request, 'registration/profile.html', context)
