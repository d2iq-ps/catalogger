"""
Script:     Catalogger App
Developer:  Dave Whitehouse - D2IQ Solutions Architect
Contact:    @dwhitehouse
Date:       7 Oct 22
Summary:    Functions to manage the session variables
"""

from flask import session
import shutil
import os

layout_dir = "/app/custom_catalogue"

def reset_session(layout_dir):
    # Resets the session
    session.clear()
    # Add starting vars
    session['gh_form_state'] = ''
    session['category_name'] = 'My Applications'
    session['gh_connected'] = 'text-grey'
    session['gh_status_message']  = 'Not Connected to a repo'
    session['gh_status_colour'] = 'text-danger'
    session['search_results'] = '<p style="padding: 10px;">Enter a search term.</p>'
    session['bundle_short'] = ''
    session['bundle_long'] = []
    session['scope'] = 'Workspace'
    session['build_enabled'] = "disabled"
    # Clear out the temporary layout directory
    shutil.rmtree(layout_dir, ignore_errors=True)
    os.makedirs(layout_dir)
    # Make a fresh repo
    new_directories = ['services', 'helm-repositories']
    for new_directory in new_directories:
        os.makedirs(f"{layout_dir}/{new_directory}")
    # Clear out icon folder
    icon_dir = '/app/templates/assets/icons'
    for f in os.listdir('/app/templates/assets/icons'):
             os.remove(os.path.join(icon_dir, f))
    # Clear out tarball folder
    icon_dir = '/app/templates/assets/tarballs'
    for f in os.listdir('/app/templates/assets/tarballs'):
             os.remove(os.path.join(icon_dir, f))
    return layout_dir


def breakout_details(key):
    '''When the users add a chart to the bundle, the checkbox ID is recovered. This is a pipe delimited list of variables which are extracted here 
    and returned as a python dictionary'''
    selection = {}
    selection['chart'] = key.split("|")[0]
    selection['version'] = key.split("|")[1]
    selection['chartID'] = key.split("|")[2]
    selection['url'] = key.split("|")[3]
    selection['repo'] = (key.split("|")[4]).replace('¬', '_').replace('[', '').replace(']', '')
    selection['description'] = (key.split("|")[5]).replace('¬', ' ')
    return selection