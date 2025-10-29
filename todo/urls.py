from django.urls import path

from todo.views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
)


app_name = "todo"

urlpatterns = [
    path("", TaskListView.as_view(), name="home"),
    path("tasks/add/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_update"),
    path("tags/", TagListView.as_view(), name="tag_list"),
    path("tags/add/", TagCreateView.as_view(), name="tag_create"),
    path("tags/<int:pk>/edit/", TagUpdateView.as_view(), name="tag_update"),
    path("tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag_delete"),
]
