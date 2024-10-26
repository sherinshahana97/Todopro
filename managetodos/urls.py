from django.urls import path
from project1 import views

urlpatterns = [
    path('', views.landingpage, name='landing_page'),  # Landing page URL
    path('login/', views.custom_login, name='login'),
    path('signup/', views.signup, name='signup'),
    
    path('logout/', views.logout_view, name='logout'),
    path('homepage/', views.homepage, name='homepage'),  # Keep your existing homepage path
  
    path('project/<int:unique_id>/', views.view_project, name='view_project'),
    path('delete_project/<str:unique_id>/', views.delete_project, name='delete_project'),
    path('todo/update/<int:todo_id>/',views.update_todo, name='update_todo'),
    path('todo/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('project/<str:unique_id>/update-title/', views.update_project_title, name='update_project_title'),
    path('project/<str:unique_id>/export_as_markdown/', views.export_as_markdown, name='export_as_markdown'),
]
