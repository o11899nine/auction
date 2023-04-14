from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit_page, name="edit_page"),
    path("search", views.search, name="search"),
    path("random", views.random_page, name="random_page"),
    path("new_page", views.new_page, name="new_page"),
]
