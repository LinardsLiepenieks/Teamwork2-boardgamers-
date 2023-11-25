from django.urls import path

from . import views

app_name = "boardgames"

urlpatterns = [
    path('', views.index, name="index")
]
