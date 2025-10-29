from django.shortcuts import render
from django.views import generic

from todo.models import Task, Tag

class TaskListView(generic.ListView):
    model = Task
    template_name = "todo/task_list.html"
    context_object_name = "tasks"
    queryset = Task.objects.prefetch_related("tags").all().order_by("is_done", "-created_at")

