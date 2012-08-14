Splunk App for Boundary - Enables Boundary Annotations & Alerts from Splunk.

.. image:: https://secure.travis-ci.org/ampledata/splunk_app_boundary.png?branch=develop
        :target: https://secure.travis-ci.org/ampledata/splunk_app_boundary

Installation
============
#. Retrieve `Boundary API Credentials`_ (API key & Organization ID).
#. Install App (from `Splunk Base`_ or from archive).
#. Add API Credentials.

.. _Boundary API Credentials: https://app.boundary.com/docs/api_access
.. _Splunk Base: http://splunk-base.splunk.com/


Usage
=====

Event Annotation
----------------
#. Search for Events within Splunk.
#. Click the 'workflow' pulldown and select **Boundary Annotation**.
.. image:: https://raw.github.com/ampledata/splunk_app_boundary/develop/docs/annotate.png

Saved Search Alert Annotation
-----------------------------
#. Created a Splunk Saved Search.
#. Under *Alert Actions* select *Run a script*.
#. Enter **boundary.py** and click *Save*.

.. image:: https://github.com/ampledata/splunk_app_boundary/blob/develop/docs/alert.png


Author
------
Greg Albrecht <mailto:gba@splunk.com>


Copyright
---------
Copyright 2012 Splunk, Inc.


License
-------
Apache License 2.0
