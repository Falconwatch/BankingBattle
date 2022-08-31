from .models import Team

def get_teams(user_id = None, game_id=None, state = "active"):
    if user_id and game_id:
        return Team.objects.filter(users_in_team__id=user_id) \
                .filter(game__id=game_id) \
                .filter(state=state) \
                .first()
    if user_id:
        return Team.objects.filter(users_in_team__id=user_id).filter(state=state).all()
    if game_id:
        return Team.objects.filter(game__id=game_id).filter(state=state).all()
    return None

def get_applications(user_id = None, game_id=None):
    return get_teams(user_id, game_id, state="application")

def get_created_teams(creator_id = None, game_id = None, state = "active"):
    if creator_id and game_id:
        print(creator_id, game_id)
        return Team.objects.filter(creator__id=creator_id)\
            .filter(game__id = game_id)\
            .filter(state = state)\
            .first()

def get_created_application(creator_id = None, game_id = None):
    return get_created_teams(creator_id=creator_id, game_id=game_id, state="application")
