from django.contrib import admin
from .models import Game, Team, Round, Dataset, Submit, TeamInvitation

# Register your models here.
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Round)
admin.site.register(Dataset)
admin.site.register(Submit)
admin.site.register(TeamInvitation)