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

Copy `.env.example` to `.env` and fill in the values from your Kinde `App Keys` page:

```console
$ cp .env.example .env
```

`.env` is already in `.gitignore`, so your secrets stay out of git.

### Environment variables

- **KINDE_CLIENT_ID** - Your Kinde client ID
- **KINDE_CLIENT_SECRET** - Your Kinde client secret
- **KINDE_HOST** - Your Kinde domain with `https://` (e.g. `https://your-subdomain.kinde.com`)
- **KINDE_REDIRECT_URI** - The callback URL: `http://localhost:5001/callback`
- **SECRET_KEY** - A random key for Flask sessions. Generate one with `python -c "import secrets; print(secrets.token_hex(32))"`

For the Management API pages (`/helpers` and `/api_demo`), also set:

- **KINDE_DOMAIN** - Your Kinde domain without `https://` (e.g. `your-subdomain.kinde.com`)
- **KINDE_MANAGEMENT_CLIENT_ID** - Your Kinde management client ID
- **KINDE_MANAGEMENT_CLIENT_SECRET** - Your Kinde management client secret

## Set your Callback and Logout URLs

Your user will be redirected to Kinde to authenticate. After they have logged in or registered they will be redirected back to your Flask application.

You need to specify in Kinde which URL you would like your user to be redirected to in order to authenticate your app.

On the App Keys page set `Allowed callback URLs` to `http://localhost:5001/callback`

> Important! This is required for your users to successfully log in to your app.

You will also need to set the URL they will be redirected to upon logout. Set the `Allowed logout redirect URLs` to `http://localhost:5001`.

## Start the app

Run `flask run` and navigate to `http://localhost:5001`.

The app runs on port 5001 because port 5000 is used by AirPlay on macOS. The port and host are set in `.env` (`FLASK_RUN_PORT` and `FLASK_RUN_HOST`).

> Open the app at `http://localhost:5001`, not `http://127.0.0.1:5001`. Your browser keeps separate cookies for the two, so if you start the login on one and Kinde sends you back to the other, the login fails with an invalid state error.

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
