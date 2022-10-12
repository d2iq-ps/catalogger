"""
Script:     Catalogger App
Developer:  Dave Whitehouse - D2IQ Solutions Architect
Contact:    @dwhitehouse
Date:       7 Oct 22
Summary:    A simple web application to automate building custom catalogues for DKP
"""

from flask import Flask, request, redirect, url_for, render_template, session, Response, send_from_directory
from githubconnect import connect_github, repo_init
from helmsearch import get_helmcharts
from jinja2 import Environment, FileSystemLoader
from sessionmanager import reset_session
from bundlemanager import bundle_add, build_out
from thumbnailer import build_gallery
import os

app = Flask(__name__, static_folder="templates/assets")
app.secret_key  = 'Dy4OvQsxcW7WH3U1aXyL52KFEgy9sxiP'
layout_dir = "/app/custom_catalogue"
tarball_dir = '/app/templates/assets/tarballs'
UPLOAD_FOLDER = '/app/templates/assets/icons'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
tar_name = "custom_catalogue.tar"

# Define jinja environment
environment = Environment(loader=FileSystemLoader("/app/templates"))


@app.before_first_request
def init_app():
    '''Set our session variables when we first load the page. Resets the github status if we have a hangover session'''
    reset_session(layout_dir)

@app.route('/')
def main():
    # Render the main page
    return render_template("index.html", 
                           state=session.get('gh_form_state'), 
                           connected=session.get('gh_connected'), 
                           gh_status_message=session.get('gh_status_message'), 
                           gh_status_colour=session.get('gh_status_colour'),
                           search_results=session.get('search_results'),
                           bundle_short = session.get('bundle_short'),
                           build_enabled = session.get('build_enabled'),
                           image_gallery = build_gallery(UPLOAD_FOLDER)
                           )

@app.route('/github', methods=['POST'])
def github():
    '''Parse the submitted data from the Github connect form and set the relevant session vars'''
    # Iterate the submitted form values and set key, values for github
    connect_github()
    return redirect(url_for('main'))
    # return render_template("index.html", state=gh_form_state, connected=gh_connected, gh_status_message=gh_status_message, gh_status_colour=gh_status_colour)

@app.route('/reset', methods=['GET'])
def reset():
    '''Reset the session'''
    reset_session(layout_dir)
    return redirect(url_for('main'))

@app.route('/helmsearch', methods=['POST'])
def helm_search():
    '''Search Artifact hub for charts'''
    search_vars={"search_term": "", "search_official": "false", "search_deprecated": "false", "search_operators": "false"}
    for key, value in request.form.items():
        search_vars[key]=value
    search_results = get_helmcharts(search_term=search_vars['search_term'], search_official=search_vars['search_official'], 
                                    search_deprecated=search_vars['search_deprecated'], search_operators=search_vars['search_operators'])
    session['search_results'] = search_results
    return redirect(url_for('main'))

@app.route('/addbundle', methods=['POST'])
def add_to_bundle():
    # Pull back our selections from the search that were added
    bundle_add(layout_dir, environment)
    return redirect(url_for('main'))


@app.route('/_set_category', methods=['GET'])
def set_category():
     session['category_name'] = request.args.get('a')
     return redirect(url_for('main'))
 
@app.route('/_set_scope', methods=['GET'])
def set_scope():
     session['scope'] = request.args.get('a')
     return redirect(url_for('main'))

@app.route('/upload', methods=['POST'])
def upload_image():
    files = request.files.getlist('file')
    for file in files:
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('main'))

@app.route('/build_bundle', methods=['GET'])
def build_bundle():
    build_out(uploads=UPLOAD_FOLDER, environment=environment, tarname=tar_name, layout_dir=layout_dir)
    try:
        gh_status = repo_init(session['gh_repo_name'])
    except:
        gh_status = 'No Github connection request was made'
    git_msg = gh_status
    return render_template('success.html', git_msg=git_msg)

@app.route('/download')
def download_tar():
    return send_from_directory('/home/dswhitehouse/catalogger//app/templates/assets/tarballs', 'custom_catalogue.tar')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
