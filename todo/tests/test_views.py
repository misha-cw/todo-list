from django.test import TestCase
from django.urls import reverse

from todo.models import Task, Tag


class TaskListViewTests(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Work")
        self.tag2 = Tag.objects.create(name="Personal")
        self.task1 = Task.objects.create(content="Task 1", is_done=False)
        self.task1.tags.add(self.tag1)
        self.task2 = Task.objects.create(content="Task 2", is_done=True)
        self.task2.tags.add(self.tag2)
        self.url = reverse("todo:home")
    
    def test_task_list_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/task_list.html")
        self.assertIn(self.task1, response.context["tasks"])
        self.assertIn(self.task2, response.context["tasks"])
    
    def test_task_list_view_post_toggle_status(self):
        self.assertFalse(self.task1.is_done)
        response = self.client.post(self.url, {"task_id": self.task1.id})
        self.assertEqual(response.status_code, 200)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_done)


class TaskCreateViewTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Urgent")
        self.url = reverse("todo:task_create")
    
    def test_task_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/task_form.html")
    
    def test_task_create_view_post(self):
        data = {
            "content": "New Task",
            "is_done": False,
            "tags": [self.tag.id],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(content="New Task").exists())
        
    def test_task_create_view_post_invalid(self):
        data = {
            "content": "", 
            "is_done": False,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "content", "This field is required.")


class TaskUpdateViewTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Chores")
        self.task = Task.objects.create(content="Old Task", is_done=False)
        self.task.tags.add(self.tag)
        self.url = reverse("todo:task_update", args=[self.task.id])
    
    def test_task_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/task_form.html")
    
    def test_task_update_view_post(self):
        new_tag = Tag.objects.create(name="Home")
        data = {
            "content": "Updated Task",
            "is_done": True,
            "tags": [new_tag.id],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, "Updated Task")
        self.assertTrue(self.task.is_done)
        self.assertIn(new_tag, self.task.tags.all())
    
    def test_task_update_view_post_invalid(self):
        data = {
            "content": "", 
            "is_done": False,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "content", "This field is required.")


class TaskDeleteViewTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(content="Task to be deleted", is_done=False)
        self.url = reverse("todo:task_delete", args=[self.task.id])
    
    def test_task_delete_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/task_confirm_delete.html")
    
    def test_task_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class TagListViewTests(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")
        self.url = reverse("todo:tag_list")
    
    def test_tag_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/tag_list.html")
        self.assertIn(self.tag1, response.context["tags"])
        self.assertIn(self.tag2, response.context["tags"])

    
class TagCreateViewTests(TestCase):
    def setUp(self):
        self.url = reverse("todo:tag_create")
    
    def test_tag_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/tag_form.html")
    
    def test_tag_create_view_post(self):
        data = {"name": "New Tag"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tag.objects.filter(name="New Tag").exists())
        
    def test_tag_create_view_post_invalid(self):
        data = {"name": ""} 
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")


class TagUpdateViewTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Old Tag")
        self.url = reverse("todo:tag_update", args=[self.tag.id])
    
    def test_tag_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/tag_form.html")
    
    def test_tag_update_view_post(self):
        data = {"name": "Updated Tag"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated Tag")
    
    def test_tag_update_view_post_invalid(self):
        data = {"name": ""} 
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "name", "This field is required.")

class TagDeleteViewTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Tag to be deleted")
        self.url = reverse("todo:tag_delete", args=[self.tag.id])
    
    def test_tag_delete_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/tag_confirm_delete.html")
    
    def test_tag_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())
