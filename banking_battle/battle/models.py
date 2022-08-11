from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Game(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=3000)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=256)
    id = models.BigAutoField(primary_key=True)
    users_in_team = models.ManyToManyField(User, related_name='users_teams')
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Round(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, related_name='rounds')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Dataset(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=1024)
    round = models.ForeignKey(Round, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name







