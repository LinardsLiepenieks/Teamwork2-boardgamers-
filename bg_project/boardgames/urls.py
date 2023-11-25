from django.urls import path
from . import views

app_name = 'boardgames'

urlpatterns = [
    path('', views.index, name='index'),
    path('boardgames/', views.boardgame_list, name='boardgame_list'),
    path('boardgames/<int:boardgame>/', views.boardgame_borrowers, name='boardgame_borrowers'),
    path('new_boardgame/', views.new_boardgame, name='new_boardgame'),
    path('new_borrowing/<int:boardgame_id>/', views.new_borrowing, name='new_borrowing'),
    path('return_boardgame/<int:borrowing_id>/', views.return_boardgame, name='return_boardgame'),
]
