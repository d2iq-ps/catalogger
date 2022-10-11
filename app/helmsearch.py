"""
Script:     Catalogger App
Developer:  Dave Whitehouse - D2IQ Solutions Architect
Contact:    @dwhitehouse
Date:       7 Oct 22
Summary:    A function that returns helm charts found in artifact hub based upon arguments provided by the user
"""

import requests
import json
import pandas as pd
import re

style_substitutions = (
    # ('<td>([\w\d].*-.*-.*-.*)</td>', '<td class=\"hidden\">\\1</td>'),
    # ('<tr>\n *<td class=\"hidden\">(.*)</td>', '<tr name=\\1>'),
    ('<th>Package ID</th>', ''),
    # ('<th>package_id', '<th class="hidden">package_id'),
    ('class="dataframe"', 'class="table table-striped"'),
    ('<th>Description', '<th style="width: 275px;">Description'),
    ('<th>Repo', '<th style="width: 125px;">Repo'),
    ('table border="1"', 'table'),
    ('<thead>', '<thead class="text-start text-secondary" style="font-size: 14px;">'),
    ('<tr style="text-align: right;">', '<tr>'),
    ('<td>True', '<td class="text-center">✔️'),
    ('<td>False', '<td class="text-center">❌'),
    ('<td>([\d\.]*)<\/td>', '<td class=\"text-center\">\\1</td>'),
    # ('></td>', '><input type="checkbox" class="upload_trigger" name="test"/></td>'),
    ('<td>\|(.*)\|</td>', '<td class=\"text-center\"><input type=\"checkbox\" class=\"upload_trigger\" name=\\1></td>'),
    ('<td>NaN', '<td class="text-left">Unofficial'),
    ('<td>False', '<td class="text-center">❌')
)

def substitute_styles(table):
    '''Accept an html table as an argument and substitutes html based on the style_substitution dict'''
    for html_from, html_to in style_substitutions:
        table = re.sub(html_from, html_to, table, re.M)
        print(f"Replaced {html_from} with {html_to}")
    return table

def get_helmcharts(search_term, search_official='false', search_deprecated='false', search_operators='false'):
    '''Search Artifact Hub for helm charts based on user search criteria'''
    headers = {
        'accept': 'application/json'
    }

    params = {
        'ts_query_web': search_term,
        'deprecated': search_deprecated,
        'operators': search_operators,
        'official': search_official,
        'facets': 'false',
        'sort': 'stars',
        'limit': '5',
        'offset': '0',
    }

    response = json.loads(requests.get('https://artifacthub.io/api/v1/packages/search', params=params, headers=headers).text)
    if not len(response['packages']):
        return '<p style="padding: 10px;">Your search yielded no results. Check your spelling or uncheck filter checkboxes.</p>'
    else:
        df = pd.json_normalize(response['packages']).fillna("Unofficial")
        df['description'] = df['description'].str.replace(' ', '¬')
        df['repository.organization_display_name'] = df['repository.organization_display_name'].str.replace(' ', '¬')
        df = df.rename(columns={'normalized_name': 'Name', 'description': 'Description', 
                        'repository.organization_display_name': "Repo",
                        'version': 'Version', 'deprecated': "Deprecated", 
                        'repository.official': 'Official', 'repository.verified_publisher': 'Verified',
                        'repository.url': 'URL', 'package_id': 'Package ID'})
        df = df.assign(Include="")
        df['Add'] = "|" + df['Name'] + "|" + df['Version'] + "|" + df['Package ID'] + "|" + df['URL'] + "|" + df['Repo'] + "|" + df['Description'] + "|"
        df['Description'] = df['Description'].str.replace('¬', ' ')
        df['Repo'] = df['Repo'].str.replace('¬', ' ')
        df = df[['Name', 'Repo', 'Description', 'Version', 'Official', 'Verified', 'Deprecated', 'URL', 'Add']].to_html(index=False, escape=True)
        df = substitute_styles(df)

        return df
