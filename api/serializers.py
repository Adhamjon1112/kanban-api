from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .exception_handler import BaseCustomException
from .models import Board, Column, Task, Subtask


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'name'] 

    def validate(self, data):
        
        print("def ichidagi data", data)

        if "id" in data.keys():
            print("id if ichidagi",data.keys())
            raise BaseCustomException("Board ID must be null while saving", 400)

    def create(self, validated_data):

        board_id = self.context['board_id']
        board = Board.objects.get(id=board_id)
        column = Column.objects.create(**validated_data)
        column.board.add(board)
        return column

class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'columns']


    def create(self, validated_data):
        columns_data = validated_data.pop('columns')

        board = Board.objects.create(**validated_data)

        for column_data in columns_data:
            column = Column.objects.create(**column_data)
            column.board.add(board)

        return board
    
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.column = validated_data.get('column', instance.column)
        instance.save()

        for subtask_data in subtasks_data:
            subtask, created = Subtask.objects.update_or_create(
                id=subtask_data.get('id'),
                task=instance,
                defaults=subtask_data
            )
        
        return instance


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'name']
    
    def create(self, validated_data):
        task_id = self.context.get('task_id')  
        task = Task.objects.get(id=task_id) 
    
        return Subtask.objects.create(task=task, **validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.task = validated_data.get('task', instance.task)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True)
    column = serializers.PrimaryKeyRelatedField(queryset=Column.objects.all())  

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'subtasks', 'column']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        board_id = self.context.get('board_id')  
        if board_id:
            self.fields['column'].queryset = Column.objects.filter(board__id=board_id)    


    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', []) 
        task = Task.objects.create(**validated_data)  

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task
    
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.column = validated_data.get('column', instance.column)
        instance.save()

        if subtasks_data is not None:
            instance.subtasks.all().delete() 
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=instance, **subtask_data)

        return instance
    