from flask import Blueprint

#auth blueprint, jusy like the views blueprint, both of them will have different views or different urls difined
#debug helps automatically rerun the server once updated, but when there's syntax error, may need to manually rerun again
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login</p"

@auth.route('/logout')
def logout():
    return "<p>Logout</p"

@auth.route('/sign-up')
def sign_up():
    return "<p>Sign Up</p"