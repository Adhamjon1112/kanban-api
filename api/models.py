from django.db import models



class Board(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Column(models.Model):
    name = models.CharField(max_length=50)
    board = models.ManyToManyField(Board, related_name='columns')

    def __str__(self):
        return self.name

class Task(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    name = models.CharField(max_length=50)
