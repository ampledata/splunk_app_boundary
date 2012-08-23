#!/usr/bin/env python
"""Boundary Splunk Setup REST Handler."""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import logging
import os
import shutil

import splunk.admin


class ConfigBoundaryApp(splunk.admin.MConfigHandler):
    """Boundary Splunk Setup REST Handler."""

    def setup(self):
        if self.requestedAction == splunk.admin.ACTION_EDIT:
            self.supportedArgs.addOptArg('api_key')
            self.supportedArgs.addOptArg('organization_id')

    def handleList(self, confInfo):
        conf = self.readConf('boundary')
        if conf is not None:
            for stanza, settings in conf.items():
                for key, val in settings.items():
                    confInfo[stanza].append(key, val)

    def handleEdit(self, confInfo):
        if self.callerArgs.data['api_key'][0] in [None, '']:
            self.callerArgs.data['api_key'][0] = ''
        if self.callerArgs.data['organization_id'][0] in [None, '']:
            self.callerArgs.data['organization_id'][0] = ''

        self.writeConf('boundary', 'api', self.callerArgs.data)
        install_boundary_py(os.environ.get('SPLUNK_HOME'))


def install_boundary_py(splunk_home):
    """Copies boundary.py to Splunk's bin/scripts directory."""
    script_src = os.path.join(
        splunk_home, 'etc', 'apps', 'splunk_app_boundary', 'bin',
        'boundary.py')
    script_dest = os.path.join(splunk_home, 'bin', 'scripts')

    logging.info(
        "Copying script_src=%s to script_dest=%s" %
        (script_src, script_dest))
    shutil.copy(script_src, script_dest)


if __name__ == '__main__':
    splunk.admin.init(ConfigBoundaryApp, splunk.admin.CONTEXT_NONE)
