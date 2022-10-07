"""
Script:     Catalogger App
Developer:  Dave Whitehouse - D2IQ Solutions Architect
Contact:    @dwhitehouse
Date:       7 Oct 22
Summary:    A simple web application to automate building custom catalogues for DKP
"""

from flask import Flask, flash, request, redirect, url_for, render_template, session, jsonify, send_file
from flask_session import Session
from flask_bootstrap import Bootstrap
from github_connect import CatalogRepo
from flask_wtf import FlaskForm
import os

# For testing, load env variables rather than reading from disk
token = os.getenv('TOKEN')
username = os.getenv('USER_NAME')
repo_name = os.getenv("REPO_NAME")

app = Flask(__name__)
Session(app)

@app.route("/", methods=['POST', 'GET'])
def main_page():
    return render_template("index.html")


c = CatalogRepo(username, token, repo_name)

if c.check_creds():
    print("Connected to Github")
else:
    print("Failed to connect to Github")


if __name__ == '__main__':
    app.run(host='0.0.0.0')