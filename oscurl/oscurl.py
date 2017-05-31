#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import logging
import os
import pprint
import sys
import time

import os_client_config
import pbr
from six.moves import http_client as httplib
from six.moves.urllib import parse as urlparse
import yaml


logging.basicConfig()
LOG = logging.getLogger('oscurl')

VERSION = pbr.version.VersionInfo('oscurl').version_string_with_vcs()


def patch_send():
    old_send = httplib.HTTPConnection.send

    def new_send(self, data):
        print('==== HTTP REQUEST ====\n%s\n==== HTTP RESPONSE ====' %
              data.decode())
        return old_send(self, data)

    httplib.HTTPConnection.send = new_send


def format_response_top(obj):
    version = obj.raw.version
    status = obj.status_code
    reason = obj.reason
    if version == 9:
        version_str = 'HTTP/0.9'
    elif version == 10:
        version_str = 'HTTP/1.0'
    elif version == 11:
        version_str = 'HTTP/1.1'
    return '%s %d %s' % (version_str, status, reason)


def format_response_headers(obj):
    header_string = ""
    for key, value in obj.items():
        header_string += "%s: %s\n" % (key, value)
    return header_string


def get_client(cloud_config, options):
    cloud = cloud_config.get_one_cloud(argparse=options)
    try:
        return cloud.get_session_client(options.service)
    except os_client_config.exceptions.OpenStackConfigException as e:
        print('''\
Error occurs during authentication.

For most cases it is due to missing OS_* environment variables.
Check OS_ environment variables for authentication are set
(like OS_AUTH_URL/OS_TENANT_NAME/OS_USERNAME/OS_PASSWORD or OS_CLOUD).

Actual exception: %s''' % e)
        sys.exit(1)


def do_request(body, cloud_config, options):
    client = get_client(cloud_config, options)

    method = options.method.upper()
    endpoint = client.get_endpoint()
    # If the base URL (the first parameter) does not end with /
    # urlparse.urljoin drops the last component of endpoint.
    # We need to ensure / exists at the last to keep the base URL.
    endpoint = endpoint.rstrip('/') + '/'
    # If the second parameter passed to urljoin starts with /,
    # it will be passed as an absolute path.
    # Otherwise, it will be interpreted as relative.
    if options.full_path:
        path = '/' + options.full_path.lstrip('/')
    else:
        path = options.path.lstrip('/')

    url = urlparse.urljoin(endpoint, path)

    if options.debug:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    show_request = options.show_mode == 'ALL'
    show_resp_header = options.show_mode in ['ALL', 'RESP']
    show_resp_body = options.show_mode in ['ALL', 'RESP', 'BODY']

    if show_request:
        patch_send()

    headers = {}
    if options.micro_version:
        headers['OpenStack-Api-Version'] = '%s %s' % (options.service,
                                                      options.micro_version)
        if options.service == 'compute':
             headers['X-Openstack-Nova-Api-Version'] = options.micro_version
    response = client.request(url, method, data=body, headers=headers,
                              raise_exc=False)

    if show_resp_header:
        print(format_response_top(response))
        print(format_response_headers(response.headers))

    if show_resp_body:
        dump_body(response, options.body_format)


def dump_body(response, body_format):
    if body_format == 'RAW':
        print(response.content)
        return

    # YAML or JSON format
    try:
        data = response.json()
    except ValueError:
        # Output raw data as fallback
        msg = '[!!!] Non-JSON data is returned. Displaying raw data.'
        print('-' * len(msg), file=sys.stderr)
        print(msg, file=sys.stderr)
        print('-' * len(msg), file=sys.stderr)
        pprint.pprint(response.content)
        return
    if body_format == 'YAML':
        print(yaml.safe_dump(data, encoding='utf-8'))
    else:
        print(json.dumps(response.json(), sort_keys=True, indent=2))


def string_lower(s):
    return s.lower()


def string_upper(s):
    return s.upper()


def main():

    default_service = os.environ.get('OSCURL_SERVICE', 'compute')
    supported_methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE']
    default_method = os.environ.get('OSCURL_METHOD', 'GET')
    supported_formats = ['RAW', 'YAML', 'JSON']
    default_format = os.environ.get('OSCURL_FORMAT', 'RAW')
    supported_show_modes = ['ALL', 'RESP', 'BODY']
    default_show_mode = 'ALL'

    parser = argparse.ArgumentParser(description='oscurl %s' % VERSION)
    parser.add_argument("--full-help",
                        action="store_true",
                        help=("Show full help message "
                              "including os-client-config options."))
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="debug mode")
    parser.add_argument("-v", "--version", action="version", version=VERSION)
    parser.add_argument("-s", "--service",
                        help=("service type (like volume, image, "
                              "identity, compute, and network). "
                              "default=%s (env[OSCURL_SERVICE] or compute)"
                              % default_service),
                        type=string_lower,
                        default=default_service)
    parser.add_argument("-V", "--micro-version",
                        default='latest',
                        help=("API microversion to be used, "
                              "default=latest"))
    parser.add_argument("-m", "--method",
                        help=("request method, "
                              "default=%s (env[OSCURL_METHOD] or GET)"
                              % default_method),
                        type=string_upper,
                        choices=supported_methods,
                        default=default_method)
    parser.add_argument("-p", "--path", dest="path",
                        help="path of URL relative to endpoint URL",
                        default='')
    parser.add_argument("-P", "--full-path",
                        help="full path of URL")
    parser.add_argument("-f", "--format", dest="body_format",
                        help=("format of response output, "
                              "default=%s (env[OSCURL_FORMAT] or RAW)"
                              % default_format),
                        type=string_upper,
                        choices=supported_formats,
                        default=default_format)
    parser.add_argument("-M", "--show-mode",
                        help=("Specify which part of request/response "
                              "should be displayed, "
                              "ALL (request and response), "
                              "RESP (response header and body), "
                              "BODY (response body only), "
                              "default: ALL"),
                        type=string_upper,
                        choices=supported_show_modes,
                        default=default_show_mode)
    parser.add_argument("-t", "--api",
                        choices=['public', 'internal', 'admin'],
                        help=("API type, default=public"))
    parser.add_argument("-i", "--input-file",
                        help=("JSON file which contains a request body. "
                              "'-' reads data from standard input."))

    # Use parse_known_args to show only oscurl options.
    # os_client_config provides a lot of options and
    # it might be annoying for existing oscurl users.
    # Note that all os_client_config options like --os-cloud can be used.
    options, _ = parser.parse_known_args()
    if options.full_help:
        # Add --help options to trigger os-client-config help
        sys.argv.append('--help')

    cloud_config = os_client_config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)
    options = parser.parse_args()

    # os_client_config uses --os-interface option.
    # Map --api option to --os-interface.
    if options.api:
        options.os_interface = options.api

    if options.input_file:
        if options.input_file == '-':
            body = sys.stdin.read()
        else:
            with open(options.input_file) as f:
                body = f.read()
        # Validate the body has valid JSON
        json.loads(body)
    else:
        body = None

    do_request(body, cloud_config, options)


if __name__ == '__main__':
    main()
