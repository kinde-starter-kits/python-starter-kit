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


def get_management_client():
    """
    Creates and returns a ManagementClient instance with proper error handling.
    Returns None if environment variables are missing or client creation fails.
    """
    # Validate required environment variables
    required_env_vars = ["KINDE_DOMAIN", "KINDE_MANAGEMENT_CLIENT_ID", "KINDE_MANAGEMENT_CLIENT_SECRET"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return None
    
    try:
        # Initialize ManagementClient with environment variables
        management_client = ManagementClient(
            domain=os.getenv("KINDE_DOMAIN"),
            client_id=os.getenv("KINDE_MANAGEMENT_CLIENT_ID"),
            client_secret=os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
        )
        logger.info("ManagementClient created successfully")
        return management_client
        
    except Exception as ex:
        logger.error(f"Failed to create ManagementClient: {ex}")
        return None



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
        
        try:
            # Handle async calls using event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Get claims
            data["claim"] = loop.run_until_complete(claims.get_all_claims())
            
            # Get feature flags using the feature_flags module
            flag_result = loop.run_until_complete(feature_flags.get_flag("theme", "red"))
            data["flag"] = flag_result.value if hasattr(flag_result, 'value') else flag_result
            
            bool_flag_result = loop.run_until_complete(feature_flags.get_flag("is_dark_mode", False))
            data["bool_flag"] = bool_flag_result.value if hasattr(bool_flag_result, 'value') else bool_flag_result
            
            str_flag_result = loop.run_until_complete(feature_flags.get_flag("theme", "red"))
            data["str_flag"] = str_flag_result.value if hasattr(str_flag_result, 'value') else str_flag_result
            
            int_flag_result = loop.run_until_complete(feature_flags.get_flag("competitions_limit", 10))
            data["int_flag"] = int_flag_result.value if hasattr(int_flag_result, 'value') else int_flag_result

            org_codes = loop.run_until_complete(claims.get_claim("org_codes","id_token"))
            data["user_organizations"] = org_codes
            
            loop.close()
        except Exception as e:
            logger.error(f"Error retrieving async data: {e}")
            # Set default values or handle gracefully
            data["claim"] = None
            data["flag"] = "red"
            data["bool_flag"] = False
            data["str_flag"] = "red"
            data["int_flag"] = 10
            data["user_organizations"] = []

        
        # Get organization and user organizations using Management API
        management_client = get_management_client()
        if management_client is not None:
            try:
                # Get all organizations (if you have permission)
                try:
                    all_orgs_response = management_client.get_organizations()
                    data["organization"] = all_orgs_response.organizations if hasattr(all_orgs_response, 'organizations') else []
                    logger.info(f"Retrieved {len(data['organization'])} total organizations")
                except Exception as org_ex:
                    logger.warning(f"Could not retrieve all organizations: {org_ex}")
                    data["organization"] = []
                    
            except Exception as mgmt_ex:
                logger.error(f"Management API error in helpers: {mgmt_ex}")
                data["organization"] = []
                data["user_organizations"] = []
        else:
            data["organization"] = []
           
        
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
        management_client = get_management_client()
        
        if management_client is None:
            data['is_api_call'] = False
            data['error_message'] = "Failed to initialize management client"
            return render_template(template, **data)
            
        try:
            api_response = management_client.get_users()
            logger.info(f"Management API response received: {len(api_response.users) if api_response.users else 0} users")
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
            logger.error(f"Management API error: {ex}")
            data['error_message'] = str(ex)

    return render_template(template, **data)