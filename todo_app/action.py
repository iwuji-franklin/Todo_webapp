from todo_app.models import TodoItem
from django.shortcuts import get_object_or_404
from django.contrib import messages
import random

TODO_ID_SESSION_KEY ='todo_id'

#get the current users todo id,sets new one if blank
def _todo_id(request):
    if request.session.get(TODO_ID_SESSION_KEY,'') =='':
        request.session[TODO_ID_SESSION_KEY] = _generate_todo_id()
    return request.session[TODO_ID_SESSION_KEY]

def _generate_todo_id():
    todo_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%&^&*()'
    todo_id_length = 50
    for y in range(todo_id_length):
        todo_id +=characters[random.randint(0, len(characters)-1)]
    return todo_id

# return all the items from the current users todo
def get_todo_items(request):
    return TodoItem.objects.filter(todo_id=_todo_id(request))

#add an item to the todo
def add_to_todo(request):
    postdata = request.POST.copy()
    name = postdata.get('title','')
    description = postdata.get('description','')
    due_date = postdata.get('due_date','')
    task_list = []
    for task in TodoItem.objects.all():
        task_list.append(task.name)
    if name in task_list:
        messages.error(request,'Task Name already exist')
    else:
        todo = TodoItem()
        todo.name = name
        todo.slug = name
        todo.description = description
        todo.due_date = due_date
        todo.todo_id = _todo_id(request)
        todo.status = "Pending"
        todo.save()
# return the total number of items in the user's todo
def todo_distinct_item_count(request):
    return get_todo_items(request).count()

def get_single_item(request, item_id):
    return get_object_or_404(TodoItem, id=item_id, todo_id=_todo_id(request))

#Update quantity for single item
def update_todo(request):
    postdata = request.POST.copy()
    name = postdata.get('title','')
    description = postdata.get('description','')
    item_id = postdata['item_id']
    todo_item=get_single_item(request, item_id)
    if todo_item:
        todo_item.name = name
        todo_item.slug = name
        todo_item.description = description
        todo_item.save()

def remove_from_todo(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    todo_item=get_single_item(request, item_id)
    if todo_item:
        todo_item.delete()
