"""
Script:     Catalogger App
Developer:  Dave Whitehouse - D2IQ Solutions Architect
Contact:    @dwhitehouse
Date:       7 Oct 22
Summary:    A simple web application to automate building custom catalogues for DKP
"""

from flask import Flask, request, redirect, url_for, render_template, session
from githubconnect import GithubRepo
from helmsearch import get_helmcharts
from jinja2 import Environment, FileSystemLoader
import os
import shutil

app = Flask(__name__, static_folder="templates/assets")
app.secret_key  = 'Dy4OvQsxcW7WH3U1aXyL52KFEgy9sxiP'
layout_dir = "app/tmp_layout"
# Define jinja environment
environment = Environment(loader=FileSystemLoader("app/templates"))

def reset_session():
    # Resets the session
    session.clear()
    # Add starting vars
    session['gh_form_state'] = ''
    session['gh_connected'] = 'text-grey'
    session['gh_status_message']  = 'Not Connected to a repo'
    session['gh_status_colour'] = 'text-danger'
    session['search_results'] = '<p style="padding: 10px;">Enter a search term.</p>'
    session['bundle_short'] = ''
    session['bundle_long'] = []
    # Clear out the temporary layout directory
    shutil.rmtree(layout_dir, ignore_errors=True)
    os.makedirs(layout_dir)
    # Make a fresh repo
    new_directories = ['services', 'helm-repositories']
    for new_directory in new_directories:
        os.makedirs(f"{layout_dir}/{new_directory}")
    return layout_dir
    
def breakout_details(key):
    '''When the users add a chart to the bundle, the checkbox ID is recovered. This is a pipe delimited list of variables which are extracted here 
    and returned as a python dictionary'''
    selection = {}
    selection['chart'] = key.split("|")[0]
    selection['version'] = key.split("|")[1]
    selection['chartID'] = key.split("|")[2]
    selection['url'] = key.split("|")[3]
    selection['repo'] = key.split("|")[4]
    return selection
        

@app.before_first_request
def init_app():
    '''Set our session variables when we first load the page. Resets the github status if we have a hangover session'''
    reset_session()

@app.route('/')
def main():
    '''Render the main page'''
    return render_template("index.html", 
                           state=session.get('gh_form_state'), 
                           connected=session.get('gh_connected'), 
                           gh_status_message=session.get('gh_status_message'), 
                           gh_status_colour=session.get('gh_status_colour'),
                           search_results=session.get('search_results'),
                           bundle_short = session.get('bundle_short')
                           )

@app.route('/github', methods=['POST'])
def github():
    '''Parse the submitted data from the Github connect form and set the relevant session vars'''
    # Iterate the submitted form values and set key, values for github
    github_vars={"gh_username": "", "gh_token": "", "gh_repo": ""}
    for key, value in request.form.items():
        github_vars[key]=value
    c = GithubRepo(github_vars['gh_username'], github_vars['gh_token'], github_vars['gh_repo'])
    if c.check_creds():
        print("Connected to Github")
        session['gh_form_state'] = "disabled"
        session['gh_connected'] = "text-success"
        session['gh_status_message']  = f"Connected to {github_vars['gh_username']}"
        session['gh_status_colour'] = "text-success"
        return redirect(url_for('main'))
    else:
        session['gh_form_state'] = ""
        session['gh_connected'] = "text-grey"
        session['gh_status_message']  = f"Not Connected to a repo"
        session['gh_status_colour'] = "text-danger"
        print("Failed to connect to Github")
        return redirect(url_for('main'))
    # return render_template("index.html", state=gh_form_state, connected=gh_connected, gh_status_message=gh_status_message, gh_status_colour=gh_status_colour)

@app.route('/reset', methods=['GET'])
def reset():
    '''Reset the session'''
    reset_session()
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
    for key, _ in request.form.items():
        # breakout the keys using the breakout_details function
        selected = breakout_details(key)
        short_key = selected['chart'] + ' (' + selected['version'] + ')'
        session['bundle_short'] = '-  ' + short_key + "<br>" + session['bundle_short']
        session['bundle_long'].append(key)
        # Build the directory structure
        os.makedirs(f"{layout_dir}/services/{selected['chart']}/{selected['version']}/defaults")
        # Build the template files
        template = environment.get_template("helmrepo_template.yaml")
        helm_repo = template.render(repo_name=selected['repo'], url=selected['url'])
        print(helm_repo)
        # Build the helm repository definition
        with open(f"{layout_dir}/helm-repositories/{selected['repo']}.yaml", "w") as hr_file:
            hr_file.write(helm_repo)
        

    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
