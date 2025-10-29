from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from todo.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    template_name = "todo/task_list.html"
    context_object_name = "tasks"
    queryset = Task.objects.prefetch_related("tags").all().order_by("is_done", "-created_at")


class TagListView(generic.ListView):
    model = Tag
    template_name = "todo/tag_list.html"
    context_object_name = "tags"
    queryset = Tag.objects.all().order_by("name")


class TagCreateView(generic.CreateView):
    model = Tag
    fields = ['name']
    template_name = "todo/tag_form.html"
    success_url = reverse_lazy("todo:tag_list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = ['name']
    template_name = "todo/tag_form.html"
    success_url = reverse_lazy("todo:tag_list")
