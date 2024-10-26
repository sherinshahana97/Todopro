from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Todo
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        print(fnm, emailid, pwd)
        my_user = User.objects.create_user(username=fnm, email=emailid, password=pwd)
        my_user.save()
        return redirect('/login')
    
    return render(request, 'register.html')

def custom_login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm, pwd)
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect('/homepage')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/login')
               
    return render(request, 'login.html')

@login_required(login_url='/login')
def logout_view(request):
    logout(request)  # Log the user out
    messages.success(request, 'Logged out successfully.')  # Add success message
    return redirect('/login')  # Redirect to the login page
    
   

def landingpage(request):
    return render(request, 'landing.html')

@login_required(login_url='/login')
def homepage(request):
    projects = Project.objects.all()
    
    if request.method == 'POST':
        unique_id = request.POST.get('unique_id')
        title = request.POST.get('title')

        # Create a new project
        Project.objects.create(unique_id=unique_id, title=title)

        return redirect('homepage')

    return render(request, 'homepage.html', {'projects': projects})

@login_required(login_url='/login')
def delete_project(request, unique_id):
    if request.method == "POST":
        project = get_object_or_404(Project, unique_id=unique_id)
        project.delete()
    return redirect('homepage')

@login_required(login_url='/login')
def view_project(request, unique_id):
    project = get_object_or_404(Project, unique_id=unique_id)
    todos = project.todos.all()

    if request.method == 'POST':
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')
        Todo.objects.create(project=project, description=description, due_date=due_date, status=status)
        return redirect('view_project', unique_id=unique_id)

    return render(request, 'view_project.html', {'project': project, 'todos': todos})

@login_required(login_url='/login')
def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == 'POST':
        todo.description = request.POST.get('description')
        todo.due_date = request.POST.get('due_date')
        todo.status = request.POST.get('status')
        todo.save()
        return redirect('view_project', unique_id=todo.project.unique_id)

    return render(request, 'update_todo.html', {'todo': todo})

@login_required(login_url='/login')
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    project_id = todo.project.unique_id
    todo.delete()
    return redirect('view_project', unique_id=project_id)

@login_required(login_url='/login')
def update_project_title(request, unique_id):
    project = get_object_or_404(Project, unique_id=unique_id)

    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title:
            project.title = new_title
            project.save()
            messages.success(request, 'Project title updated successfully!')
        else:
            messages.error(request, 'Title cannot be empty.')

    return redirect('view_project', unique_id=project.unique_id)


@login_required(login_url='/login')
def export_as_markdown(request, unique_id):
    project = get_object_or_404(Project, unique_id=unique_id)
    todos = Todo.objects.filter(project=project)

    completed_todos = todos.filter(status='completed')
    pending_todos = todos.filter(status='pending')

    total_todos = todos.count()
    completed_count = completed_todos.count()

    # Generate the Markdown content
    markdown_content = f"# {project.title}\n\n"  # Project title as an h1 heading
    markdown_content += f"### **Summary:** {completed_count} / {total_todos} completed.\n\n"  # Summary as bold h3

    # Section 1: Pending Todos
    markdown_content += "## **Pending:**\n\n"  # Pending section as bold h2
    for todo in pending_todos:
        markdown_content += f"- [ ] {todo.description}\n"  # Open checkbox for pending todos

    # Section 2: Completed Todos
    markdown_content += "\n## **Completed:**\n\n"  # Completed section as bold h2
    for todo in completed_todos:
        markdown_content += f"- [x] {todo.description}\n"  # Checked box for completed todos

    # Create the response
    response = HttpResponse(markdown_content, content_type='text/markdown')
    response['Content-Disposition'] = f'attachment; filename="{project.title}.md"'
    
    return response