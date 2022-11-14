from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from todo_app.forms import AddNewForm
from todo_app.models import TodoItem
from todo_app import action
from todo_project import settings
# Create your views here.


def home(request):
    #getting the total number of our tasks
    completed_list = TodoItem.objects.filter(status="Completed", todo_id=action._todo_id(request))
    pending_list = TodoItem.objects.filter(status="Pending", todo_id=action._todo_id(request))
    todo_item_count = action.todo_distinct_item_count(request)
    page_title='Todo List'
    tasks = action.get_todo_items(request)
    if request.method=="POST":
        #add to action...create the bound form
        postdata = request.POST.copy()
        
        form = AddNewForm(request, postdata)
        #check if posted data is valid
        if form.is_valid():
        #add to action and redirect to action page
            action.add_to_todo(request)
            #if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
    else:
        #it's a GET, create the unbound form.note request as a kwarg
        form = AddNewForm(request=request, label_suffix=':')
    #set the test cookie on our first GET request
    request.session.set_test_cookie()
    return render(request,'index.html',{'pending_list':pending_list, 'completed_list':completed_list, 'form':form, 'todo_item_count':todo_item_count,'tasks':tasks,'page_title':page_title})

def show_task(request, slug):
    task=TodoItem.objects.get(slug=slug)
    page_title = task.name
    todo_item_count = action.todo_distinct_item_count(request)
    tasks = action.get_todo_items(request)
    #getting related products
    # need to evaluate the HTTP method
    if request.method=="POST":
        #add to action...create the bound form
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            action.remove_from_todo(request)
            return redirect('todo_app:home')
        if postdata['submit'] == 'Update':
            action.update_todo(request)
            return redirect('todo_app:home')
    return render(request,'task.html',{'todo_item_count':todo_item_count,'tasks':tasks,'task':task,'page_title':page_title})

def change_status(request, slug):
    task=TodoItem.objects.get(slug=slug)
    page_title = task.name
    todo_item_count = action.todo_distinct_item_count(request)
    tasks = action.get_todo_items(request)
    #getting related products
    # need to evaluate the HTTP method
    if request.method=="POST":
        #add to action...create the bound form
        postdata = request.POST.copy()
        if postdata['submit'] == 'Completed':
            item_id = postdata['item_id']
            todo_item=TodoItem.objects.get(id=item_id)
            if todo_item:
                todo_item.status = "Completed"
                todo_item.save()
    return redirect('todo_app:home')
