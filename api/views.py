from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Board, Column, Task, Subtask
from .serializers import BoardSerializer, ColumnSerializer, TaskSerializer, SubtaskSerializer
from rest_framework import filters


class BoardCreateView(generics.CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['id', 'name']


class BoardUpdateView(generics.UpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDeleteView(generics.DestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class ColumnCreateView(generics.CreateAPIView):
    serializer_class = ColumnSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['board_id'] = self.kwargs.get('board_id')
        return context
    

class ColumnListView(generics.ListAPIView):
    serializer_class = ColumnSerializer

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        return Column.objects.filter(board__id=board_id)


class ColumnUpdateView(generics.UpdateAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer


class ColumnDeleteView(generics.DestroyAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['board_id'] = self.kwargs.get('board_id')
        return context


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        column_id = self.kwargs.get('column_id')
        return Task.objects.filter(column_id=column_id)


class SubtaskCreateView(generics.CreateAPIView):
    serializer_class = SubtaskSerializer

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')  
        serializer.context['task_id'] = task_id  
    
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SubtaskListView(generics.ListAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

class SubtaskDetailView(generics.RetrieveAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    lookup_field = 'id'  

class SubtaskUpdateView(generics.UpdateAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    lookup_field = 'id'  

class SubtaskDeleteView(generics.DestroyAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    lookup_field = 'id' 