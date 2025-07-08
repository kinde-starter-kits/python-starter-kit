# Kinde Starter Kit - Flask

## Register an account on Kinde

To get started set up an account on [Kinde](https://app.kinde.com/register).

## Setup your local environment

Clone this repo and install dependencies by running 
```console
$ pip install -r requirements.txt
```
The minimum required version of Python is 3.9.

## Configuration

This starter kit uses Kinde Python SDK v2, which simplifies the configuration by using environment variables instead of a config file.

Create a `.env` file in the root directory with the following variables from your Kinde `App Keys` page:

```env
# Kinde Flask Starter Kit Environment Variables
# Copy this template and fill in your actual values

# Required: Your Kinde application credentials
KINDE_CLIENT_ID=your_client_id_here
KINDE_CLIENT_SECRET=your_client_secret_here
KINDE_REDIRECT_URI=http://localhost:5000/callback
KINDE_DOMAIN=https://your-subdomain.kinde.com

# Optional: Management API credentials (for enhanced features)
KINDE_MANAGEMENT_CLIENT_ID=your_management_client_id_here
KINDE_MANAGEMENT_CLIENT_SECRET=your_management_client_secret_here

# Flask configuration
FLASK_SECRET_KEY=your-secret-key-here
```

### Required Environment Variables:

- **KINDE_CLIENT_ID** - Your Kinde client ID
- **KINDE_CLIENT_SECRET** - Your Kinde client secret  
- **KINDE_REDIRECT_URI** - The callback URL (typically `http://localhost:5000/callback`)
- **KINDE_DOMAIN** - Your Kinde domain (e.g., `https://your-subdomain.kinde.com`)
- **KINDE_MANAGEMENT_CLIENT_ID** - Your Kinde management client ID (for Management API features)
- **KINDE_MANAGEMENT_CLIENT_SECRET** - Your Kinde management client secret

> **Note**: Make sure to add `.env` to your `.gitignore` file to keep your secrets secure.

## Set your Callback and Logout URLs

Your user will be redirected to Kinde to authenticate. After they have logged in or registered they will be redirected back to your Flask application.

You need to specify in Kinde which URL you would like your user to be redirected to in order to authenticate your app.

On the App Keys page set `Allowed callback URLs` to `http://localhost:5000/callback`

> Important! This is required for your users to successfully log in to your app.

You will also need to set the URL they will be redirected to upon logout. Set the `Allowed logout redirect URLs` to `http://localhost:5000`.

## Start the app

Run `flask run` and navigate to `http://localhost:5000`.

Click on `Sign up` and register your first user for your business!

## What's New in SDK v2

This starter kit has been updated to use Kinde Python SDK v2, which includes several improvements:

- **Simplified Configuration**: No more `config.py` file - everything is configured via environment variables
- **Framework Integration**: Built-in Flask integration with automatic route registration
- **Async Support**: Better support for asynchronous operations
- **Management API**: Enhanced Management API client for user and organization management
- **Feature Flags**: Improved feature flag handling
- **Permissions**: Streamlined permission checking

## View users in Kinde

If you navigate to the "Users" page within Kinde you will see your newly registered user there. 🚀
