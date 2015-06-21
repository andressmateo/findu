from app import lm
from app.models import User
@lm.user_loader
def load_user(userid):
    return User.query.get(userid)