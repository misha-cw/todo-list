from django.test import TestCase
from todo.models import Tag, Task


class TagModelTest(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name="Urgent")
        self.assertEqual(tag.name, "Urgent")
        self.assertEqual(str(tag), "Urgent")
    
    def test_tag_string(self):
        tag = Tag.objects.create(name="Work")
        self.assertEqual(str(tag), "Work")


class TaskModelTest(TestCase):
    def test_create_task(self):
        task = Task.objects.create(content="Finish homework")
        self.assertEqual(task.content, "Finish homework")
        self.assertFalse(task.is_done)
        self.assertEqual(str(task), "Finish homework")
    
    def test_task_with_tags(self):
        tag1 = Tag.objects.create(name="Urgent")
        tag2 = Tag.objects.create(name="Home")
        task = Task.objects.create(content="Clean the house")
        task.tags.add(tag1, tag2)
        self.assertEqual(task.tags.count(), 2)
        self.assertIn(tag1, task.tags.all())
        self.assertIn(tag2, task.tags.all())

    def test_task_string(self):
        task = Task.objects.create(content="Go grocery shopping")
        self.assertEqual(str(task), "Go grocery shopping")
