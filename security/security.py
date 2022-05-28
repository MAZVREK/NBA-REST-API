from security.user import User
import hmac

# AUTHENTICATION FUNCTION REQUIRED FOR USE OF JWT
def authenticate(username, password):
    user = User.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

# IDENTITY FUNCTION REQUIRED FOR USE OF JWT
def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
