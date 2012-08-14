#!/usr/bin/env python
"""Boundary Annotations API Client for Python.

See also: https://app.boundary.com/docs/annotations
"""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import base64
import ConfigParser
import csv
import gzip
try:
    import json
except ImportError:
    import simplejson as json
import os
import traceback
import urllib2


import splunk
import splunk.Intersplunk


API_URL = 'https://api.boundary.com'


class BoundaryAnnotations(object):
    """Boundary Annotations API Client"""

    def __init__(self, organization_id, api_key):
        self.url = '/'.join([API_URL, organization_id, 'annotations'])

        # 'Python urllib2 Basic Auth Problem': http://bit.ly/KZDZNk
        b64_auth = base64.encodestring(
            ':'.join([api_key, ''])).replace('\n', '')
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
            self.url, annotation_json, {'Content-type': 'application/json'})
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', self.auth_header)
        # TODO(gba) Add error checking, since there basically isn't any.
        response = urllib2.urlopen(req)
        return json.load(response)


def gzcat(gzfile):
    """Decompresses gzip'd files, returns their content.

    @param gzfile: gzip'd file to decompress.
    @type gzfile: str

    @return: Contents of decompressed gzfile.
    @rtype: str
    """
    gzfd = gzip.open(gzfile, 'rb')
    file_content = gzfd.read()
    gzfd.close()
    return file_content


def csv_to_dict(raw_csv):
    """Deserializes CSV into native Python Dictionary.

    @param raw_csv: CSV content.
    @type raw_csv: str

    @return: CSV content as a native Python Dictionary.
    @rtype: dict
    """
    return csv.DictReader(raw_csv)


def extract_events():
    """Extracts event data from Splunk CSV file.

    @return: Events from CSV file.
    @rtype: list
    """
    events = []
    events_file = os.environ.get('SPLUNK_ARG_8')
    if events_file is not None:
        if os.path.exists(events_file):
            events = csv.DictReader(gzip.open(events_file))
    return events


def get_api_credentials():
    """Extracts Boundary API key and Organization ID from Splunk Config.

    @return: API key, Organization ID.
    @rtype: tuple
    """
    cfg_src = os.path.join(
        os.environ['SPLUNK_HOME'], 'etc', 'apps', 'splunk_app_boundary', 'local',
        'boundary.conf')
    config = ConfigParser.ConfigParser()
    config.read(cfg_src)
    return config.get('api', 'api_key'), config.get('api', 'organization_id')


def main():
    """main, duh?"""
    results = []

    api_key, organization_id = get_api_credentials()
    apiclient = BoundaryAnnotations(organization_id, api_key)

    if 'SPLUNK_ARG_1' in os.environ:
        #events = extract_events()
        annotation = {
            'type':  os.environ['SPLUNK_ARG_5'],
            'links': [
                {'rel': 'search', 'href': os.environ['SPLUNK_ARG_6']},
                {'rel': 'results', 'href': os.environ['SPLUNK_ARG_8']}
            ]
        }
        apiclient.create_annotation(annotation)
    else:
        try:
            results, _, _ = splunk.Intersplunk.getOrganizedResults()
            for result in results:
                annotation = {
                    'type': result['_raw'], 'start_time': result['_time']}
                apiclient.create_annotation(annotation)
        except Exception:
            stack = traceback.format_exc()
            results = splunk.Intersplunk.generateErrorResults(
                "Error : Traceback: " + str(stack))
        finally:
            splunk.Intersplunk.outputResults(results)


if __name__ == '__main__':
    main()
