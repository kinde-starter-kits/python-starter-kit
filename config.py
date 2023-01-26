from kinde_sdk.kinde_api_client import GrantType


SITE_HOST = "localhost"
SITE_PORT = "8080"
SITE_URL = f"http://{SITE_HOST}:{SITE_PORT}"
LOGOUT_REDIRECT_URL = f"http://{SITE_HOST}:{SITE_PORT}"
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "SOME_SECRET"
KINDE_ISSUER_URL = "https://[your_subdomain].kinde.com"
GRANT_TYPE = GrantType.AUTORIZATION_CODE
CODE_VERIFIER = "CODE_VERIFIER"
