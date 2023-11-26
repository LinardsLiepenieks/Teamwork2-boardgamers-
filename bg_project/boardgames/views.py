from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Boardgame, Borrowing
from django.contrib import messages
from .forms import BoardgameForm


def index(request):
    if request.user.is_authenticated:
        boardgames_not_owned = Boardgame.objects.exclude(user=request.user) \
            .exclude(borrowing__borrower=request.user, borrowing__date_returned__isnull=True)
    else:
        # If no user is logged in, you might handle it differently (e.g., show all board games)
        boardgames_not_owned = Boardgame.objects.exclude(
            borrowing__date_returned__isnull=True)

    return render(request, 'boardgames/index.html', {'boardgames': boardgames_not_owned})


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
        Boardgame, pk=boardgame_id)
    button = ""
    method = ""
    action = ""
    user = request.user
    if user.is_authenticated:
        if user == boardgame.user:
            method = "get"
            action = "boardgames:edit_boardgame"
            button = "Edit Boardgame"
        elif boardgame.borrowing_set.filter(borrower=user,  # type: ignore
                                            date_returned__isnull=True):
            method = "post"
            action = "boardgames:return_boardgame"
            button = "Return this Boardgame"
        else:
            method = "post"
            action = "boardgames:borrow"
            button = "Borrow this Boardgame"

    context = {}
    context['method'] = method
    context['action'] = action
    context['button'] = button
    context['boardgame'] = boardgame

    return render(request, 'boardgames/boardgame_detail.html', context)


@login_required
def edit_boardgame(request, boardgame_id):
    # Retrieve the board game object
    boardgame = get_object_or_404(
        Boardgame, pk=boardgame_id, user=request.user)

    if request.method == 'POST':
        # If the form is submitted, process the data
        form = BoardgameForm(request.POST, instance=boardgame)
        if form.is_valid():
            form.save()
            return redirect('boardgames:boardgame_detail', boardgame_id=boardgame.pk)
    else:
        # If it's a GET request, populate the form with the current board game data
        form = BoardgameForm(instance=boardgame)

    return render(request, 'boardgames/edit_boardgame.html', {'form': form, 'boardgame': boardgame})


@login_required
def borrow(request, boardgame_id):
    boardgame = get_object_or_404(Boardgame, pk=boardgame_id)
    user = request.user
    message = None

    existing_borrowing = Borrowing.objects.filter(
        boardgame=boardgame, borrower=user, date_returned__isnull=True).first()

    if existing_borrowing:
        message = "You have already borrowed this game!"
        messages.error(request, message)

    else:
        # If the user hasn't borrowed the game, create a new borrowing entry
        message = "Game borrowed!"
        messages.success(request, message)
        Borrowing.objects.create(boardgame=boardgame, borrower=user)

    return redirect('accounts:profile')


@login_required
def return_boardgame(request, boardgame_id):
    # Get the Boardgame instance or raise a 404 error
    boardgame = get_object_or_404(Boardgame, id=boardgame_id)

    # Check if the logged-in user has borrowed the Boardgame
    borrowing_record = Borrowing.objects.filter(
        boardgame=boardgame, borrower=request.user, date_returned__isnull=True).first()

    if borrowing_record:
        # Set the date_returned field to mark the Borrowing as returned
        borrowing_record.delete()
        messages.success(request, "Game returned!")

        # Redirect to a success page or another view
        return redirect('accounts:profile')
    else:
        messages.error(request, "You have not borrowed this game!")

        # Handle the case where there is no active Borrowing record for the user
        return redirect('accounts:profile')
