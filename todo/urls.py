from django.urls import path

from todo.views import (
    TaskListView,
    TagListView,
)


app_name = "todo"

urlpatterns = [
    path("", TaskListView.as_view(), name="home"),
    path("tags/", TagListView.as_view(), name="tag_list"),
]
