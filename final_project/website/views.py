# store the standard routes to our website, where the user can actually go to (pages such as home page that dont need authentications)

from flask import Blueprint, render_template

#blueprint of our applications, with all the routes

views = Blueprint('views', __name__)

@views.route('/')#put the url to get to the website, this function will run when we go to / route
def home():
    return render_template("home.html")

#then register these blueprint to __init__.py to tell flask that we have these blueprints that contains different routes or urls for applications
