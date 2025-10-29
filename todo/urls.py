from django.urls import path

from todo.views import (
    TaskListView,
    TagListView,
    TagCreateView,
)


app_name = "todo"

urlpatterns = [
    path("", TaskListView.as_view(), name="home"),
    path("tags/", TagListView.as_view(), name="tag_list"),
    path("tags/add/", TagCreateView.as_view(), name="tag_create"),
]
