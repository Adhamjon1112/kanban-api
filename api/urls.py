from django.urls import path
from .views import (BoardCreateView, BoardDeleteView, BoardListView, 
                    BoardUpdateView, ColumnCreateView, ColumnDeleteView,  
                    ColumnListView, ColumnUpdateView, SubtaskCreateView, SubtaskDeleteView, SubtaskDetailView, SubtaskListView, SubtaskUpdateView, TaskCreateView, TaskDeleteView, TaskDetailView, TaskListView, TaskUpdateView)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Hujjatlari",    
        default_version='v2',      
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('boards/', BoardListView.as_view(), name='board-list'),
    path('boards/create/', BoardCreateView.as_view(), name='board-create'),
    path('boards/<int:pk>/update/', BoardUpdateView.as_view(), name='board-update'),
    path('boards/<int:pk>/delete/', BoardDeleteView.as_view(), name='board-delete'),

    path('columns/create/<int:board_id>/', ColumnCreateView.as_view(), name='column-create'),
    path('columns/<int:board_id>/', ColumnListView.as_view(), name='column-list'),
    path('columns/<int:pk>/update/', ColumnUpdateView.as_view(), name='column-update'),
    path('columns/<int:pk>/delete/', ColumnDeleteView.as_view(), name='column-delete'),

    path('tasks/create/<int:board_id>/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:id>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:id>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<int:column_id>/', TaskListView.as_view(), name='task-list'),

    path('subtasks/create/<int:task_id>/', SubtaskCreateView.as_view(), name='subtask-create'),
    path('subtasks/', SubtaskListView.as_view(), name='subtask-list'),
    path('subtasks/<int:id>/', SubtaskDetailView.as_view(), name='subtask-detail'),
    path('subtasks/<int:id>/update/', SubtaskUpdateView.as_view(), name='subtask-update'),
    path('subtasks/<int:id>/delete/', SubtaskDeleteView.as_view(), name='subtask-delete'),

]
