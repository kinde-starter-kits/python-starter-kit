from datetime import date
from flask import Flask, url_for, render_template, request

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
}
if app.config["GRANT_TYPE"] == GrantType.AUTORIZATION_CODE_WITH_PKCE:
    kinde_api_client_params["code_verifier"] = app.config["CODE_VERIFIER"]

kinde_client = KindeApiClient(**kinde_api_client_params)


@app.route("/")
def index():
    data = {"current_year": date.today().year}
    template = "logged_out.html"
    if kinde_client.is_authenticated():
        user = kinde_client.get_user_details()
        data["user_given_name"] = user.get("given_name")
        data["user_family_name"] = user.get("family_name")
        template = "logged_in.html"
    return render_template(template, **data)


@app.route("/api/auth/login")
def login():
    return app.redirect(kinde_client.login())


@app.route("/api/auth/register")
def register():
    return app.redirect(kinde_client.register())


@app.route("/api/auth/kinde_callback")
def callback():
    kinde_client.fetch_token(authorization_response=request.url)
    return app.redirect(url_for("index"))


@app.route("/api/auth/logout")
def logout():
    return app.redirect(
        kinde_client.logout(redirect_to=app.config["LOGOUT_REDIRECT_URL"])
    )


app.run(host=app.config["SITE_HOST"], port=app.config["SITE_PORT"])
