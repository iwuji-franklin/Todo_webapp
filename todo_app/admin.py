from django.contrib import admin
from todo_app.models import TodoItem
# Register your models here.

class TodoItemAdmin(admin.ModelAdmin):
    #sets values for how the admin site lists your products
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'status']
    exclude = ('date_added', 'due_date')
    #sets up slug to be generated from product name
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(TodoItem, TodoItemAdmin)