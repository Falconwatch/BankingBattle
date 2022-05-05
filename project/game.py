from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

game = Blueprint('game', __name__)

@game.route("/game")
@login_required
def game_stats():
    return render_template('game.html')
    return "sad"