# Kinde Starter Kit - Flask

## Register an account on Kinde

To get started set up an account on [Kinde](https://app.kinde.com/register).

## Setup your local environment

Clone this repo and install dependencies by running `pip install -r requirements.txt`

Set the variables in `config.py` with the details from the Kinde `App Keys` page

> KINDE_ISSUER_URL - The token host value
>
> CLIENT_ID - The client id
>
> CLIENT_SECRET - The client secret

e.g

```
KINDE_ISSUER_URL = "https://your_kinde_subdomain.kinde.com"
CLIENT_ID = "someClientId"
CLIENT_SECRET = "some5ecretFromappKey5pag3"
```

## Set your Callback and Logout URLs

Your user will be redirected to Kinde to authenticate. After they have logged in or registered they will be redirected back to your Flask application.

You need to specify in Kinde which url you would like your user to be redirected to in order to authenticate your app.

On the App Keys page set ` Allowed callback URLs` to `http://localhost:8080/api/auth/kinde_callback`

> Important! This is required for your users to successfully log in to your app.

You will also need to set the url they will be redirected to upon logout. Set the `Allowed logout redirect URLs` to http://localhost:8080.

## Start the app

Run `flask run` and navigate to `http://localhost:8080`.

Click on `Sign up` and register your first user for your business!

## View users in Kinde

If you navigate to the "Users" page within Kinde you will see your newly registered user there. 🚀