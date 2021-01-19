from flask import Flask
from flask_login import LoginManager

from database import Database
from club import Club
from user import get_user
from os.path import expanduser
from pathlib import Path
import os
from views import home_page, eclubs_page, account_page, add_event_page, an_event_page, register_event_page
from views import events_page, join_page, login_page, login_clubs_page, logout_page, about_page, club_add_page
from views import eclub_page, register_page, register_club_page
#import views
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

    app.add_url_rule("/", view_func=home_page)
    app.add_url_rule("/eclubs", view_func=eclubs_page, methods=["GET", "POST"])
    app.add_url_rule("/account", view_func=account_page, methods=["GET", "POST"])
    app.add_url_rule("/addevent", view_func=add_event_page, methods=["GET", "POST"])
    app.add_url_rule("/anevent", view_func=an_event_page, methods=["GET", "POST"])
    app.add_url_rule("/registeredevent", view_func=register_event_page, methods=["GET", "POST"])
    app.add_url_rule("/events", view_func=events_page, methods=["GET", "POST"])
    app.add_url_rule("/joined", view_func=join_page, methods=["GET", "POST"])
    app.add_url_rule("/loginstudent", view_func=login_page, methods=["GET", "POST"])
    app.add_url_rule("/loginclub", view_func=login_clubs_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=logout_page)
    app.add_url_rule("/about", view_func=about_page)
    #app.add_url_rule("/eclub", view_func=views.eclub_page)
    app.add_url_rule(
        "/new-club", view_func=club_add_page, methods=["GET", "POST"])
    app.add_url_rule(
        "/eclub", view_func=eclub_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/registerstudent", view_func=register_page, methods=["GET", "POST"])
    app.add_url_rule("/registerclub", view_func=register_club_page, methods=["GET", "POST"])
    lm.init_app(app)
    lm.login_view = "login_page"

    #home_dir = os.path.expanduser("~")
    #db = Database(os.path.join(home_dir, "clubs.db"))
    #app.config["db"] = db
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.0", port=port)
    
    

