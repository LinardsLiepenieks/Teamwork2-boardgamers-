from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Boardgame, Borrowing
from django.contrib import messages
from .forms import BoardgameForm, BorrowingForm


def index(request):
    return render(request, 'boardgames/index.html')


@login_required
def new_boardgame(request):
    if request.method == 'POST':
        form = BoardgameForm(request.POST)
        if form.is_valid():
            new_boardgame = form.save(commit=False)
            new_boardgame.user = request.user
            new_boardgame.save()
            # Redirect to a view displaying the details of the new boardgame
            return redirect('boardgames:boardgame_detail', boardgame_id=new_boardgame.pk)
    else:
        form = BoardgameForm()

    return render(request, 'boardgames/new_boardgame.html', {'form': form})


def boardgame_detail(request, boardgame_id):
    boardgame = get_object_or_404(
        Boardgame, pk=boardgame_id, user=request.user)
    return render(request, 'boardgames/boardgame_detail.html', {'boardgame': boardgame})


def new_boardgame2(request):
    """Add a new boardgame."""
    if request.method != 'POST':
        form = BoardgameForm()
    else:
        form = BoardgameForm(data=request.POST)
        if form.is_valid():
            boardgame = form.save()

            # Verifying quantity of borrowed boardgame
            user = request.user
            if Borrowing.objects.filter(borrower=user, date_returned__isnull=True).count() >= 3:
                # If +3 chosen boardgames, retract the newest one + an error message
                boardgame.delete()
                messages.error(
                    request, "You can't borrow more than 3 boardgames at a time.")
                return redirect('boardgames:boardgame_list')

            return redirect('boardgames:boardgame_list')

    context = {'form': form}
    return render(request, 'boardgames/boardgames2.html', context)


def new_borrowing(request):
    pass
