from flask import g
from flask_login import current_user

def inject_studio():
    if current_user.is_authenticated:
        g.studio_id = current_user.studio_id
        g.studio_nome = current_user.studio.nome
    else:
        g.studio_id = None
        g.studio_nome = None
