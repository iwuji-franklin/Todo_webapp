from django.contrib.auth.models import User
from itertools import product
from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
)


class TodoItem(models.Model):
    todo_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,help_text='Unique value for product page URL, created from title.')
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')

    class Meta:
        db_table = 'Todo_items'
        ordering = ['date_added', 'status']

    def __str__(self) -> str:
        return self.title    

    def __unicode__(self):
        return self.title