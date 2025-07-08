from datetime import date
from flask import Flask, url_for, render_template, request, session
from flask_session import Session
from functools import wraps
import asyncio
import logging
import os
from dotenv import load_dotenv

# Import kinde_flask to register the Flask framework
import kinde_flask

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth import claims, feature_flags, permissions, tokens
from kinde_sdk.management import ManagementClient;

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Kinde OAuth with Flask framework
kinde_oauth = OAuth(
    framework="flask",
    app=app
)

def get_authorized_data():
    logger.info("get_authorized_data: Starting authentication check")
    
    if not kinde_oauth.is_authenticated():
        logger.warning("get_authorized_data: User is not authenticated")
        return None
    
    logger.info("get_authorized_data: User is authenticated, getting user info")
    user = kinde_oauth.get_user_info()
    logger.info(f"get_authorized_data: User: {user}")
    
    if not user:
        logger.warning("get_authorized_data: Failed to get user info")
        return None
    
    logger.info(f"get_authorized_data: Successfully retrieved user info for user ID: {user.get('id', 'unknown')}")
    logger.info(f"get_authorized_data: Full user data: {user}")
    id_token = tokens.get_token_manager().get_id_token()
    logger.info(f"get_authorized_data: ID token: {id_token}")
    access_token = tokens.get_token_manager().get_access_token()
    logger.info(f"get_authorized_data: Access token: {access_token}")
    claims = tokens.get_token_manager().get_claims()
    logger.info(f"get_authorized_data: Claims: {claims}")
    
    user_data = {
        "id": user.get("id"),
        "user_given_name": user.get("given_name"),
        "user_family_name": user.get("family_name"),
        "user_email": user.get("email"),
        "user_picture": user.get("picture"),
    }
    
    logger.info(f"get_authorized_data: Returning user data: {user_data}")
    return user_data



@app.route("/")
def index():
    data = {"current_year": date.today().year}
    template = "logged_out.html"
    if kinde_oauth.is_authenticated():
        data.update(get_authorized_data())        
        template = "home.html"
    return render_template(template, **data)



@app.route("/details")
def get_details():
    template = "logged_out.html"
    data = {"current_year": date.today().year}

    if kinde_oauth.is_authenticated():
        data = {"current_year": date.today().year}
        data.update(get_authorized_data())
        data["access_token"] = tokens.get_token_manager().get_access_token()
        template = "details.html"

    return render_template(template, **data)


@app.route("/helpers")
def get_helper_functions():
    template = "logged_out.html"

    data = {"current_year": date.today().year}

    if kinde_oauth.is_authenticated():
        data.update(get_authorized_data())
        #print(kinde_client.configuration.access_token)
        
        # Handle async calls using event loop
        loop = asyncio.get_event_loop()
        
        # Get claims
        data["claim"] = loop.run_until_complete(claims.get_all_claims("iss"))
        
        # Get feature flags using the feature_flags module
        data["flag"] = loop.run_until_complete(feature_flags.get_flag("theme", "red"))
        data["bool_flag"] = loop.run_until_complete(feature_flags.get_flag("is_dark_mode", False))
        data["str_flag"] = loop.run_until_complete(feature_flags.get_flag("theme", "red"))
        data["int_flag"] = loop.run_until_complete(feature_flags.get_flag("competitions_limit", 10))
        
        # Note: Organization methods are not available in the current OAuth class
        # You would need to use the Management API or implement custom methods
        # data["organization"] = kinde_client.get_organization()
        # data["user_organizations"] = kinde_client.get_user_organizations()
        
        template = "helpers.html"

    else:
        template = "logged_out.html"

    return render_template(template, **data)

@app.route("/api_demo")
def get_api_demo():
    template = "api_demo.html"

    data = {"current_year": date.today().year}
    data.update(get_authorized_data())
    if kinde_oauth.is_authenticated():
        try:
            # Initialize ManagementClient with environment variables
            management_client = ManagementClient(
                domain=os.getenv("KINDE_DOMAIN"),
                client_id=os.getenv("KINDE_MANAGEMENT_CLIENT_ID"),
                client_secret=os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
            )
            api_response = management_client.get_users()
            print(f"Management API not setup: {api_response}")
            data['users'] = [
                {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'total_sign_ins': int(user.total_sign_ins)
                }
                for user in api_response.users
            ]
            data['is_api_call'] = True
            
        except Exception as ex:
            data['is_api_call'] = False
            print(f"Management API not setup: {ex}")

    return render_template(template, **data)