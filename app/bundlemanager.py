"""
Script:     Catalogger App
Developer:  Dave Whitehouse - D2IQ Solutions Architect
Contact:    @dwhitehouse
Date:       7 Oct 22
Summary:    Functions that trigger when adding an item to a bundle
"""

from flask import session, request, flash
from sessionmanager import breakout_details
import os
from os import listdir
import base64
import re
import tarfile

default_image = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pg0KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE5LjAuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPg0KPHN2ZyB2ZXJzaW9uPSIxLjEiIGlkPSJDYXBhXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4Ig0KCSB2aWV3Qm94PSIwIDAgNTUgNTUiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDU1IDU1OyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+DQo8cGF0aCBzdHlsZT0iZmlsbDojRUZDRTRBOyIgZD0iTTIxLjY2LDI0SDIuMzRDMS4wNDgsMjQsMCwyMi45NTIsMCwyMS42NlYyLjM0QzAsMS4wNDgsMS4wNDgsMCwyLjM0LDBoMTkuMzINCglDMjIuOTUyLDAsMjQsMS4wNDgsMjQsMi4zNHYxOS4zMkMyNCwyMi45NTIsMjIuOTUyLDI0LDIxLjY2LDI0eiIvPg0KPHBhdGggc3R5bGU9ImZpbGw6IzdGQUJEQTsiIGQ9Ik01MS42NiwyNEgzMi4zNEMzMS4wNDgsMjQsMzAsMjIuOTUyLDMwLDIxLjY2VjIuMzRDMzAsMS4wNDgsMzEuMDQ4LDAsMzIuMzQsMGgxOS4zMg0KCUM1Mi45NTIsMCw1NCwxLjA0OCw1NCwyLjM0djE5LjMyQzU0LDIyLjk1Miw1Mi45NTIsMjQsNTEuNjYsMjR6Ii8+DQo8cGF0aCBzdHlsZT0iZmlsbDojRDc1QTRBOyIgZD0iTTIxLjY2LDU0SDIuMzRDMS4wNDgsNTQsMCw1Mi45NTIsMCw1MS42NlYzMi4zNEMwLDMxLjA0OCwxLjA0OCwzMCwyLjM0LDMwaDE5LjMyDQoJYzEuMjkyLDAsMi4zNCwxLjA0OCwyLjM0LDIuMzR2MTkuMzJDMjQsNTIuOTUyLDIyLjk1Miw1NCwyMS42Niw1NHoiLz4NCjxsaW5lIHN0eWxlPSJmaWxsOm5vbmU7c3Ryb2tlOiMyM0EyNEQ7c3Ryb2tlLXdpZHRoOjI7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MTA7IiB4MT0iNDIiIHkxPSIzMCIgeDI9IjQyIiB5Mj0iNTQiLz4NCjxsaW5lIHN0eWxlPSJmaWxsOm5vbmU7c3Ryb2tlOiMyM0EyNEQ7c3Ryb2tlLXdpZHRoOjI7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MTA7IiB4MT0iMzAiIHkxPSI0MiIgeDI9IjU0IiB5Mj0iNDIiLz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjwvc3ZnPg0K"

def build_out(uploads):
    tar_name = "custom_catalogue.tar"
    # Get our image names
    image_matches = []
    image_list = []
    for image in listdir(uploads):
        image_list.append(image)
    # Get our chart names
    chart_names = []
    for key in session['bundle_long']:
        chart_name = key.split('|')[0]
        chart_names.append(chart_name)
    # Iterate through each chart to see if there is an image match. If so, wirte it to image_matches array
    for chart in chart_names:
        for image in image_list:
            if image.find(chart) == 0:
                image_matches.append({'chart': chart, 'image': image})
    # Update our b64 images in the metadata file
    for image_match in image_matches:
        with open(f"{uploads}/{image_match['image']}", "rb") as vector_image:
            encoded_image = str(base64.b64encode(vector_image.read()))[2:-1]
        # Replace the default icon with the one uploaded
            with open(f"app/custom_catalogue/services/{image_match['chart']}/metadata.yaml", "r+") as metadata_file:
                search_string = r"icon\: (.*)"
                content = metadata_file.read()
                replacement_string = f"icon: {encoded_image}"
                content_new = re.sub(search_string, replacement_string, content, 0, re.MULTILINE)
                metadata_file.seek(0)
                metadata_file.write(content_new)
                metadata_file.truncate()
    # Finally, build a tarball in case the user choses to download
    with tarfile.open(f"app/templates/assets/tarballs/{tar_name}", "w:gz") as tar:
        source_dir = 'app/custom_catalogue'
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return image_matches


def bundle_add(layout_dir, environment):
    for key, _ in request.form.items():
        # breakout the keys using the breakout_details function
        selected = breakout_details(key)
        short_key = selected['chart'] + ' (' + selected['version'] + ')'
        if len(session['bundle_short']) == 0:
            session['bundle_short'] = f"Bundled Applications:<br>"
        session['bundle_short'] = session['bundle_short'] + '&nbsp;&nbsp;- ' + short_key + "<br>"
        session['bundle_long'].append(key)
        # Build the directory structure
        os.makedirs(f"{layout_dir}/services/{selected['chart']}/{selected['version']}/defaults")
        # Build a blank config file
        open(f"{layout_dir}/services/{selected['chart']}/{selected['version']}/defaults/cm_{selected['chart']}", "x")
        # Build the template files
        # helm repository definition
        template = environment.get_template("helmrepo_template.yaml")
        helm_repo = template.render(repo_name=selected['repo'], url=selected['url'])
        with open(f"{layout_dir}/helm-repositories/{selected['repo']}.yaml", "w") as hr_file:
            hr_file.write(helm_repo)
        # helm release definition
        template = environment.get_template("helmrelease_template.yaml")
        helm_release = template.render(name=selected['chart'], chart_name=selected['chart'], version=selected['version'], repo=selected['repo'])
        with open(f"{layout_dir}/services/{selected['chart']}/{selected['version']}/{selected['chart']}.yaml", "w") as hr_file:
            hr_file.write(helm_release)
        # kustomize for the helm release
        template = environment.get_template("customization_template_hr.yaml")
        helm_release_k = template.render(helmrelease_file=f"{selected['chart']}.yaml")
        with open(f"{layout_dir}/services/{selected['chart']}/{selected['version']}/kustomization.yaml", "w") as hr_file:
            hr_file.write(helm_release_k)
        # kustomize for the configmap
        template = environment.get_template("customization_template_cm.yaml")
        helm_release_c = template.render(cm_file=f"cm_{selected['chart']}.yaml")
        with open(f"{layout_dir}/services/{selected['chart']}/{selected['version']}/defaults/kustomization.yaml", "w") as hr_file:
            hr_file.write(helm_release_c)
        # metadata definition
        template = environment.get_template("metadata_template.yaml")
        # Check if we have a better image available or else use the default svg
        
        metadata = template.render(display_name=selected['chart'], overview=selected['description'], description=selected['description'], category=session['category_name'], scope=session['scope'], icon=default_image)
        with open(f"{layout_dir}/services/{selected['chart']}/metadata.yaml", "w") as hr_file:
            hr_file.write(metadata)
        session['build_enabled'] = ''
