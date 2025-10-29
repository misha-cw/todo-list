from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from todo.models import Task, Tag
from todo.forms import TaskForm


class TaskListView(generic.View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.prefetch_related("tags").all().order_by("is_done", "-created_at")
        return render(request, "todo/task_list.html", {"tasks": tasks})
    
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get("task_id")
        task = Task.objects.get(id=task_id)
        task.is_done = not task.is_done
        task.save()
        tasks = Task.objects.prefetch_related("tags").all().order_by("is_done", "-created_at")
        return render(request, "todo/task_list.html", {"tasks": tasks})

class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("todo:home")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("todo:home")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "todo/task_confirm_delete.html"
    success_url = reverse_lazy("todo:home")


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


class TagDeleteView(generic.DeleteView):
    model = Tag
    template_name = "todo/tag_confirm_delete.html"
    success_url = reverse_lazy("todo:tag_list")
