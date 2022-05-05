from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

game = Blueprint('game', __name__)

@game.route("/game/resuls")
@login_required
def game_results():
    return render_template('game_results.html')

@game.route("/game")
@login_required
def game_main():
    return render_template('game.html')

@game.route("/game/leaders")
@login_required
def game_leaders():
    return render_template('game_leaders.html')
