from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify, session
from spotify import (
    authenticate_with_spotify,
    get_access_token,
    spotify_get_playlist,
    spotify_refresh_token,
)
from datetime import datetime
import os
import redis
import Spotify
import Apple
import Youtube


app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv("SERVER_SECRET", default="NO_KEY")

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.from_url("redis://127.0.0.1:6379")


def token_expired():
    if "expires_at" in session:
        return datetime.now().timestamp() > session["expires_at"]
    return True


def get_expires_at(num_seconds):
    return datetime.now().timestamp() + num_seconds


@app.route("/")
def index():
    return """
    Welcome to MusicSo 
    <br>
    <a href='/login-spotify'> Login With Spotify </a>
    <br>
    <a href='/login-apple'> Login With Apple </a>
    <br>
    <a href='/login-youtube'>Login with Youtube Music </a>
    """


@app.route("/login-spotify")
def loginSpotify():
    sp = Spotify()
    return redirect(sp.authenticate)


@app.route("/login-apple")
def loginApple():
    sp = Apple()
    return redirect(sp.authenticate)


@app.route("/login-youtube")
def loginYoutube():
    sp = Youtube()
    return redirect(sp.authenticate)


@app.route("/success")
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})
    if "code" in request.args:
        token_info = get_access_token(request.args["code"])

    session["access_token"] = token_info["access_token"]
    session["refresh_token"] = token_info["refresh_token"]
    session["expires_at"] = get_expires_at(token_info["expires_in"])
    return redirect("/playlists")


@app.route("/playlists")
def get_playlists():
    if "access_token" not in session:
        return redirect("/login")
    if token_expired():
        return redirect("/refresh-token")
    return spotify_get_playlist(session["access_token"])


@app.route("/refresh-token")
def refresh_token():
    if "refresh_token" not in session:
        return redirect("/login")

    if token_expired():
        new_token_info = spotify_refresh_token(session["refersh_token"])
        session["access_token"] = new_token_info["access_token"]
        session["expires_at"] = get_expires_at(new_token_info["expires_in"])

    return redirect("/playlists")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


# store tokens in redis or sqlite
# add user to neo4j with music provider
# add songs to neo4j
