from flask import request
from users.data_access import *
from auth.core import permission, verify_email_token, revoke_auth_token
from auth.utils import *
from basehandler import api_response
from errors.v1.handlers import *
from users.data_access import UserDacc


def signup(**kwargs: dict):
    data = kwargs['body']

    pwd = prep_password(data['password'])

    # Swap the password in data for the hashed one
    data['password'] = pwd
    UserDacc.signup(data)

    return api_response()


def login(**kwargs: dict):
    auth = kwargs['body']
    email = auth['email'].lower()
    password = auth['password']

    uid, token, refresh_token = UserDacc.login(email, password)
    return api_response({'token': token, 'refresh_token': refresh_token, 'user_id': uid, 'email': email})


def logout(**kwargs):
    if 'Authorization' in request.headers:

        # Extract auth data from the authentication header
        auth_data = request.headers['Authorization'].encode('ascii', 'ignore').decode('ascii')

        # Check there is a Bearer token
        if 'Bearer ' in auth_data:
            token = auth_data.replace('Bearer ', '')
            kwargs['token_info']['token'] = token

            permission(kwargs['token_info'], access_role='basic', logout=True)
            UserDacc.logout(kwargs['token_info']['user_id'])
            return api_response()
        else:
            raise ApiError(message="Authorisation required", status_code=400)

    raise ApiError(message="User NOT logged out", status_code=400)


def email_verification(**kwargs):
    try:
        payload = verify_email_token(kwargs['token'])
        UserDacc.verify_email(payload['user_id'], payload['email_claim'])
        revoke_auth_token(kwargs['token'])
        return api_response()
    except Exception:
        raise ApiError('authorisation-required', status_code=401)


def generate_new_tokens(**kwargs: dict) -> dict:
    """
        Generates new API usage and refresh tokens
        Generally when a client's access token has expired they can request a
        new set of tokens be generated as long as they have the correct unexpired
        refresh token.

    :param user_id: The ID of the user to generate new tokens for.
    :param kwargs:
    :return: tokens
    :errors:
        'unknown-user' 404
    """
    permission(kwargs['token_info'], access_role='basic')
    token, refresh_token = UserDacc.generate_new_tokens(kwargs['token_info']['user_id'], kwargs['old_access_token'])
    return api_response({'token': token, 'refresh_token': refresh_token, 'user': kwargs['token_info']['user_id']})

