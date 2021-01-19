from flask import Flask
from flask_login import LoginManager

from database import Database
from club import Club
from user import get_user
from os.path import expanduser
from pathlib import Path
import os
import views
import forms
app = Flask(__name__)
app.secret_key = "super secret key"
url = os.getenv("DATABASE_URL")
lm = LoginManager()
#lm.init_app(app)

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)



def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/events", view_func=views.eclubs_page, methods=["GET", "POST"])
    app.add_url_rule("/account", view_func=views.account_page, methods=["GET", "POST"])
    app.add_url_rule("/addevent", view_func=views.add_event_page, methods=["GET", "POST"])
    app.add_url_rule("/anevent", view_func=views.an_event_page, methods=["GET", "POST"])
    app.add_url_rule("/registeredevent", view_func=views.register_event_page, methods=["GET", "POST"])
    app.add_url_rule("/eclubs", view_func=views.events_page, methods=["GET", "POST"])
    app.add_url_rule("/joined", view_func=views.join_page, methods=["GET", "POST"])
    app.add_url_rule("/loginstudent", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/loginclub", view_func=views.login_clubs_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/about", view_func=views.about_page)
    #app.add_url_rule("/eclub", view_func=views.eclub_page)
    app.add_url_rule(
        "/new-club", view_func=views.club_add_page, methods=["GET", "POST"])
    app.add_url_rule(
        "/eclub", view_func=views.eclub_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/registerstudent", view_func=views.register_page, methods=["GET", "POST"])
    app.add_url_rule("/registerclub", view_func=views.register_club_page, methods=["GET", "POST"])
    #♀lm.init_app(app)
    #lm.login_view = "login_page"

    #home_dir = os.path.expanduser("~")
    #db = Database(os.path.join(home_dir, "clubs.db"))
    #app.config["db"] = db
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)
    
    

