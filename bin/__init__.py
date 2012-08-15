#!/usr/bin/env python
"""Splunk App for Boundary."""

__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


from .boundary import (get_api_credentials, search_command, alert_command,
    get_config_file, setup_apiclient, main)
