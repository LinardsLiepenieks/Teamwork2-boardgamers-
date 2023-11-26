from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from boardgames.models import Boardgame
from django.contrib import messages


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
def profile(request, message=""):
    context = {}
    context['message'] = message
    context['user'] = request.user
    context['boardgames'] = Boardgame.objects.filter(user=context['user'])
    borrowed_boardgames = Boardgame.objects.filter(
        borrowing__borrower=context['user'], borrowing__date_returned__isnull=True)
    context['borrowed_boardgames'] = borrowed_boardgames
    message = messages.get_messages(request)
    context['message'] = message

    return render(request, 'registration/profile.html', context)
