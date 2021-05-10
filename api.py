import os
from werkzeug.exceptions import abort
from db import fetch_user_from_discord_user_id
from flask import request
from main import app, get_conn

API_KEY = os.environ['API_KEY']
if len(API_KEY) < 30:
  print("API_KEY env variable must be at least 30 characters long")
  quit()

@app.route('/api/<string:discord_user_id>')
def api(discord_user_id: str):
  # Check API key
  provided_api_key = request.args.get('api_key')

  if not provided_api_key == API_KEY:
    abort(401)
  
  conn = get_conn()
  user = fetch_user_from_discord_user_id(conn, discord_user_id)

  if not user:
    abort(404)

  return user