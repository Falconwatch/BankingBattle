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
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=256, default="application")
    #задуманные состояния application - заявка на создание команды, active - команда активна, другие
    #ToDo: перевести состояния в Enum???

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


class Submit(models.Model):
    id = models.BigAutoField(primary_key=True)
    submission_dt = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submits/')
    result = models.DecimalField(default=0, decimal_places=2, max_digits=19)


    class Meta:
        ordering = ['team']

    def __str__(self):
        return str(self.file)

class Invitation(models.Model):
    id = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=256, default="incoming") #incoming - пользователь просится в команду, outcoing - пользователя приглашают в команду
    state = models.CharField(max_length=256, default="pending") #pending - ожидает решения, inactive - решение было принято