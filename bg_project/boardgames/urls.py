from django.urls import path
from . import views

app_name = 'boardgames'

urlpatterns = [
    path('', views.index, name='index'),
    # path('boardgames/', views.boardgame_list, name='boardgame_list'),
    # path('boardgames/<int:boardgame>/', views.boardgame_borrowers, name='boardgame_borrowers'),
    path('new_boardgame/', views.new_boardgame, name='new_boardgame'),
    path('edit_boardgame/<int:boardgame_id>/',
         views.edit_boardgame, name='edit_boardgame'),
    path('boardgames/<int:boardgame_id>',
         views.boardgame_detail, name="boardgame_detail"),
    path('boardgames/<int:boardgame_id>/borrow/',
         views.borrow, name="borrow"),
    path('boardgames/<int:boardgame_id>/return/',
         views.return_boardgame, name="return_boardgame")
    # path('return_boardgame/<int:borrowing_id>/', views.return_boardgame, name='return_boardgame'),
]
