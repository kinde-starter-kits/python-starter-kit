from datetime import date
from flask import Flask, url_for, render_template, request
from functools import wraps

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient


app = Flask(__name__)
app.config.from_object("config")

configuration = Configuration(host=app.config["KINDE_ISSUER_URL"])
kinde_api_client_params = {
    "configuration": configuration,
    "domain": app.config["KINDE_ISSUER_URL"],
    "client_id": app.config["CLIENT_ID"],
    "client_secret": app.config["CLIENT_SECRET"],
    "grant_type": app.config["GRANT_TYPE"],
    "callback_url": app.config["KINDE_CALLBACK_URL"],
}
if app.config["GRANT_TYPE"] == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
    kinde_api_client_params["code_verifier"] = app.config["CODE_VERIFIER"]

kinde_client = KindeApiClient(**kinde_api_client_params)


def get_authorized_data(kinde_client):
    user = kinde_client.get_user_details()
    return {
        "user_given_name": user.get("given_name"),
        "user_family_name": user.get("family_name"),
        "user_email": user.get("email"),
        "user_picture": user.get("picture"),
    }


def login_required(user):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user.is_authenticated():
                return app.redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route("/")
def index():
    data = {"current_year": date.today().year}
    template = "logged_out.html"
    if kinde_client.is_authenticated():
        data.update(get_authorized_data(kinde_client))        
        template = "home.html"
    return render_template(template, **data)


@app.route("/api/auth/login")
def login():
    return app.redirect(kinde_client.get_login_url())


@app.route("/api/auth/register")
def register():
    return app.redirect(kinde_client.get_register_url())


@app.route("/api/auth/kinde_callback")
def callback():
    kinde_client.fetch_token(authorization_response=request.url)
    return app.redirect(url_for("index"))


@app.route("/api/auth/logout")
def logout():
    return app.redirect(
        kinde_client.logout(redirect_to=app.config["LOGOUT_REDIRECT_URL"])
    )


@app.route("/details")
@login_required(kinde_client)
def get_details():
    data = {"current_year": date.today().year}
    data.update(get_authorized_data(kinde_client))
    data["access_token"] = kinde_client.configuration.access_token
    template = "details.html"
    return render_template(template, **data)


@app.route("/helpers")
@login_required(kinde_client)
def get_helper_functions():
    data = {"current_year": date.today().year}
    data.update(get_authorized_data(kinde_client))
    data["claim"] = kinde_client.get_claim("iss")
    data["organization"] = kinde_client.get_organization()
    data["user_organizations"] = kinde_client.get_user_organizations()
    data["flag"] = kinde_client.get_flag("theme")
    data["bool_flag"] = kinde_client.get_boolean_flag("is_dark_mode")
    data["str_flag"] = kinde_client.get_string_flag("theme")
    data["int_flag"] = kinde_client.get_integer_flag("competitions_limit")
    template = "helpers.html"
    return render_template(template, **data)
