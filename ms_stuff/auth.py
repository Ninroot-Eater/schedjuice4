from tkinter.messagebox import NO
import msal
import os
import json
from decouple import config
from .config import settings

"""
These are basically copied from here: https://docs.microsoft.com/en-us/graph/tutorials/python?tutorial-step=3
With some slight modifications.
"""


def load_cache(request):
    cache = msal.SerializableTokenCache()
    if request.session.get("token_cache"):
        cache.deserialize(request.session["token_cache"])
    
    return cache

def save_cache(request, cache):

    if cache.has_state_changed:
        request.session["token_cache"] = cache.serialize()


def get_msal_app(cache=None,daemon=False):

    if daemon:
        app = msal.ConfidentialClientApplication(
            settings["app_id"],
            authority=settings["authority"],
            
            client_credential={
                "thumbprint": settings["thumbprint"],
                "private_key": open(settings['private_key_file']).read()
                },

        )
        return app
    
    auth_app = msal.ClientApplication(
        settings["app_id"],
        authority=settings["authority"],
        client_credential=config("CLIENTSEC"),
        token_cache=cache
    )
    
    return auth_app


def get_sign_in_flow():
    auth_app = get_msal_app()
    return auth_app.initiate_auth_code_flow(
        settings["scopes"],
        redirect_uri=settings["redirect"]
    )

def get_token_from_code(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)

    flow = request.session.pop("auth_flow", {})
    result =  auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
    save_cache(request, cache)

    return result


def store_user(request, user):
    try:
        if "mailboxSettings" in user:
            t = user["mailboxSettings"]["timeZone"]
        else:
            t = "UTC"
        request.session['MSuser'] = {
      'is_authenticated': True,
      'name': user['displayName'],
      'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName'],
      'timeZone': t
    },
    except Exception as e:
        print("ERROR",e)


def get_token(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)
    
    accounts = auth_app.get_accounts()
    
    if accounts:
        result = auth_app.acquire_token_silent(
            settings["scopes"],
            account = accounts[0]
        )
        save_cache(request, cache)
        return result["access_token"]


def remove_user_and_token(request):
    if "token_cache" in request.session:
        del request.session["token_cache"]

    if "MSuser" in request.session:
        del request.session["MSuser"]






    


