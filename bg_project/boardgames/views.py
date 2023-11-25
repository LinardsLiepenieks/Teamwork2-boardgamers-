from django.shortcuts import render, redirect
from .models import Boardgame, Borrowing
from django.contrib import messages
from .forms import BoardgameForm, BorrowingForm

def index(request):
    return render(request, 'boardgames/index.html')

def new_boardgame(request):
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
                messages.error(request, "You can't borrow more than 3 boardgames at a time.")
                return redirect('boardgames:boardgame_list')

            return redirect('boardgames:boardgame_list')

    context = {'form': form}
    return render(request, 'boardgames/boardgames2.html', context)