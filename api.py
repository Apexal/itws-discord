import os
from flask_cas import login_required
from werkzeug.exceptions import abort
from db import fetch_user_from_api_key, fetch_user_from_discord_user_id
from flask import request
from main import app, get_conn


@app.route('/api/<string:discord_user_id>')
def api(discord_user_id: str):
  # Check API key
  provided_api_key = request.args.get('api_key')
  
  conn = get_conn()
  
  # User making the request
  request_user = fetch_user_from_api_key(conn, provided_api_key)

  if not request_user:
    abort(401)
  
  target_user = fetch_user_from_discord_user_id(conn, discord_user_id)
  app.logger.info(
    f'{request_user["rcs_id"]} requested the details for {target_user["rcs_id"]}')

  if not target_user:
    abort(404)

  # Purposefully whitelist fields returned
  # (don't return api_key!)
  return {
    'rcs_id': target_user['rcs_id'],
    'first_name': target_user['first_name'],
    'last_name': target_user['last_name'],
    'graduation_year': target_user['graduation_year'],
    'is_faculty': target_user['is_faculty']
  }