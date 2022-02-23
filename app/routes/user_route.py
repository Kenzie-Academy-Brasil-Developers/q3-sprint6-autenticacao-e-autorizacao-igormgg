from flask import Blueprint

from app.controllers.user_controller import (delete_user, get_user, login_user,
                                             register_user, update_user)

bp_user = Blueprint("bp_user", __name__, url_prefix="/api")

bp_user.post('/signup')(register_user)
bp_user.post('/signin')(login_user)
bp_user.get('')(get_user)
bp_user.put('')(update_user)
bp_user.delete('')(delete_user)