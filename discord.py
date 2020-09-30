from http.client import responses
import os
from typing import Dict
import requests
from dotenv import load_dotenv
load_dotenv()

API_BASE = 'https://discordapp.com/api'
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
CLIENT_SECRET = os.environ.get('DISCORD_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('DISCORD_REDIRECT_URI')
SERVER_ID = os.environ.get('DISCORD_SERVER_ID')
VERIFIED_ROLE_ID = os.environ.get('DISCORD_VERIFIED_ROLE_ID')
HEADERS = {
    'Authorization': 'Bot ' + BOT_TOKEN,
}

OAUTH_URL = f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=guilds.join%20identify'


def get_tokens(code):
    '''
    Given an authorization code, request the access and refresh tokens for a Discord user.
    Returns the tokens. Throws an error if invalid request.
    '''
    response = requests.post(f'{API_BASE}/oauth2/token',
                             data={
                                 'client_id': CLIENT_ID,
                                 'client_secret': CLIENT_SECRET,
                                 'grant_type': 'authorization_code',
                                 'code': code,
                                 'redirect_uri': REDIRECT_URI,
                                 'scope': 'identity guilds.join'
                             },
                             headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             }
                             )
    response.raise_for_status()
    tokens = response.json()
    return tokens


def get_user_info(access_token):
    '''
    Given an access token, get a Discord user's info including id, username, discriminator, avatar url, etc.
    Throws an error if invalid request.
    '''
    response = requests.get(f'{API_BASE}/users/@me', headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    )
    response.raise_for_status()
    user = response.json()
    return user


def get_member(user_id: str) -> Dict:
    '''Retreive a server member. Includes the user, their server nickname, roles, etc.'''
    response = requests.get(
        f'{API_BASE}/guilds/{SERVER_ID}/members/{user_id}', headers=HEADERS)
    response.raise_for_status()
    return response.json()


def add_user_to_server(access_token: str, user_id: str, nickname: str):
    '''
    Given a Discord user's id, add them to the Discord server with their nickname
    set as their RCS ID and with the verified role.
    '''
    response = requests.put(f'{API_BASE}/guilds/{SERVER_ID}/members/{user_id}',
                            json={
                                'access_token': access_token,
                                'nick': nickname,
                                'roles': [VERIFIED_ROLE_ID],
                            },
                            headers=HEADERS
                            )
    response.raise_for_status()
    return response


def kick_member_from_server(user_id: str):
    '''Remove a user from the server.'''
    response = requests.delete(
        f'{API_BASE}/guilds/{SERVER_ID}/members/{user_id}', headers=HEADERS)
    response.raise_for_status()
    return response


def set_member_nickname(user_id: str, nickname: str):
    '''Given a Discord user's id, set their nickname on the server.'''
    response = requests.patch(f'{API_BASE}/guilds/{SERVER_ID}/members/{user_id}',
                              json={
                                  'nick': nickname
                              },
                              headers=HEADERS
                              )
    response.raise_for_status()
    return response


def add_role_to_member(user_id: str, role_id: str):
    '''Add a role (identified by its id) to a member.'''
    response = requests.put(
        f'{API_BASE}/guilds/{SERVER_ID}/members/{user_id}/roles/{role_id}', headers=HEADERS)
    response.raise_for_status()
    return response


def remove_role_from_member(user_id: str, role_id: str):
    '''Remove a role (identified by its id) from a member.'''
    response = requests.delete(
        f'{API_BASE}/guilds/{SERVER_ID}/members/{user_id}/roles/{role_id}', headers=HEADERS)
    response.raise_for_status()
    return response
