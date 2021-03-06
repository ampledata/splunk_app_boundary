#!/usr/bin/env python
"""Boundary Annotations API Client for Python.

See also: https://app.boundary.com/docs/annotations
"""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import base64
import ConfigParser
try:
    import json
except ImportError:
    import simplejson as json  # pylint: disable=F0401
import os
import traceback
import urllib2


API_URL = 'https://api.boundary.com'


class BoundaryAnnotations(object):
    """Boundary Annotations API Client"""

    def __init__(self, organization_id, api_key):
        self.url = '/'.join([API_URL, organization_id, 'annotations'])

        # 'Python urllib2 Basic Auth Problem': http://bit.ly/KZDZNk
        b64_auth = base64.encodestring(
            ':'.join([api_key, ''])
        ).replace('\n', '')

        self.auth_header = ' '.join(['Basic', b64_auth])

    def create_annotation(self, annotation):
        """Creates an Annotation in Boundary.

        @param annotation: Annotation Params per
            https://app.boundary.com/docs/annotations
        @type annotation: dict

        @return: Response from Boundary.
        @rtype: dict
        """
        annotation_json = json.dumps(annotation)

        req = urllib2.Request(
            self.url, annotation_json, {'Content-type': 'application/json'}
        )

        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', self.auth_header)

        # TODO(gba) Add error checking, since there basically isn't any.
        response = urllib2.urlopen(req)

        return json.load(response)


def get_api_credentials(config_file):
    """Extracts Boundary API key and Organization ID from Splunk Config.

    @return: API key, Organization ID.
    @rtype: tuple
    """
    api_credentials = ()
    if config_file is not None and os.path.exists(config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        api_credentials = (
            config.get('boundary_api', 'api_key'),
            config.get('boundary_api', 'organization_id')
        )
    return api_credentials


def search_command(apiclient):
    """Invokes Boundary Annotations as a Search Command."""
    import splunk
    import splunk.Intersplunk

    try:
        results, _, _ = splunk.Intersplunk.getOrganizedResults()
        for result in results:
            annotation = {
                'type': result['_raw'], 'start_time': result['_time']
            }
            apiclient.create_annotation(annotation)
    # TODO(gba) Catch less general exception.
    except Exception:
        stack = traceback.format_exc()
        results = splunk.Intersplunk.generateErrorResults(
            "Error : Traceback: " + str(stack)
        )
    finally:
        splunk.Intersplunk.outputResults(results)


def alert_command(apiclient):
    """Invokes Boundary Annotations as a Saved-Search Alert Command."""
    annotation = {
        'type':  os.environ.get('SPLUNK_ARG_5'),
        'links': [
            {'rel': 'search', 'href': os.environ.get('SPLUNK_ARG_6')},
            {'rel': 'results', 'href': os.environ.get('SPLUNK_ARG_8')}
        ]
    }
    return apiclient.create_annotation(annotation)


def get_config_file():
    """Gets Boundary Config File location.

    @return: Path to Boundary Config File.
    @rtype: str
    """
    config_file = 'boundary.conf'
    splunk_home = os.environ.get('SPLUNK_HOME')

    if splunk_home is not None and os.path.exists(splunk_home):
        _config_file = os.path.join(
            splunk_home, 'etc', 'apps', 'splunk_app_boundary', 'local',
            'boundary.conf')
        if os.path.exists(_config_file):
            config_file = _config_file

    return config_file


def setup_apiclient():
    """Sets up Boundary API Instance."""
    api_key, organization_id = get_api_credentials(get_config_file())
    return BoundaryAnnotations(organization_id, api_key)


def main():
    """Differentiates alert invocation from search invocation."""
    if 'SPLUNK_ARG_1' in os.environ:
        alert_command(setup_apiclient())
    else:
        search_command(setup_apiclient())


if __name__ == '__main__':
    main()
