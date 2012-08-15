#!/usr/bin/env python
"""Tests for Splunk App for Boundary. """

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import ConfigParser
import os
import random
import shutil
import tempfile
import unittest

from .context import bin


class TestBoundary(unittest.TestCase):
    """Tests for Splunk App for Boundary."""

    def setUp(self):
        self.config_file = tempfile.mkstemp()[1]
        self.events_file = tempfile.mkstemp()[1]
        self.rands = ''.join(
            [random.choice('unittest0123456789') for xyz in range(8)])
        self.rand_row = [self.rands, self.rands]

    def _setup_splunk_home(self):
        self.raw_config = 'default/boundary.conf'
        self.raw_boundary_py = 'bin/boundary.py'

        self.splunk_home = tempfile.mkdtemp()

        self.pd_app = os.path.join(
            self.splunk_home, 'etc', 'apps', 'boundary')
        self.pd_bin = os.path.join(self.pd_app, 'bin')
        self.pd_default = os.path.join(self.pd_app, 'default')
        self.spl_scripts = os.path.join(
            self.splunk_home, 'bin', 'scripts')

        os.makedirs(self.pd_bin)
        os.makedirs(self.pd_default)
        os.makedirs(self.spl_scripts)

        shutil.copyfile(self.raw_config, self.config_file)
        shutil.copy(self.raw_boundary_py, self.pd_bin)

    def test_get_service_api_key(self):
        rand_api_key = '_'.join(['org', 'key', self.rands])
        rand_org_id = '_'.join(['org', 'id', self.rands])

        self._setup_splunk_home()
        config = ConfigParser.RawConfigParser()

        config.read(self.config_file)
        config.set('api', 'api_key', rand_api_key)
        config.set('api', 'organization_id', rand_org_id)

        with open(self.config_file, 'wb') as cfg:
            config.write(cfg)

        api_key, organization_id = bin.boundary.get_api_credentials(
            self.config_file)

        self.assertEqual(api_key, rand_api_key)
        self.assertEqual(organization_id, rand_org_id)
