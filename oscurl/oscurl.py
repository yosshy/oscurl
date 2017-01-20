#!/usr/bin/env python

import argparse
import fileinput
import httplib
import json
import logging
import os
import sys
import time
import urlparse

import os_client_config
import yaml


logging.basicConfig()
LOG = logging.getLogger('oscurl')


def error_exit(message):
    sys.stdout.flush()
    LOG.error(message)
    sys.exit(1)


def patch_send():
    old_send = httplib.HTTPConnection.send

    def new_send(self, data):
        print('==== HTTP REQUEST ====\n%s\n==== HTTP RESPONSE ====' % data)
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
        print 'Error occurs during authentication.'
        print 'For most cases it is due to missing OS_* environment variables.'
        print 'Check OS_ environment variables for authentication are set.'
        print ('(like OS_AUTH_URL/OS_TENANT_NAME/OS_USERNAME/OS_PASSWORD '
               'or OS_CLOUD)')
        sys.exit(1)


def do_request(body, cloud_config, options):
    client = get_client(cloud_config, options)

    if options.delay:
        time.sleep(65)

    method = options.method.upper()
    endpoint = client.get_endpoint()
    path = endpoint + options.path

    if options.full_path:
        path = options.full_path
        o = urlparse.urlparse(endpoint)
        path = "%s://%s%s" % (o.scheme, o.netloc, options.full_path)

    if options.debug:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    response = client.get(path, data=body)
    response.raise_for_status()

    format = options.format
    response_top = format_response_top(response)
    response_headers = format_response_headers(response.headers)
    if format == 'RAW':
        print(response_top)
        print(response_headers)
        print(response.content)
    elif format == 'HEADER':
        print(response_top)
        print(response_headers)
    elif format == 'BODY':
        print(response.content)
    elif format == 'YAML':
        print(response_top)
        print(response_headers)
        if not response.content:
            return
        print(yaml.safe_dump(response.json(), encoding='utf-8'))
    elif format == 'JSON':
        print(response_top)
        print(response_headers)
        if not response.content:
            return
        print(json.dumps(response.json(), sort_keys=True, indent=2))


def main():

    default_service = os.environ.get('OSCURL_SERVICE', 'compute')
    supported_methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE']
    default_method = os.environ.get('OSCURL_METHOD', 'GET')
    supported_formats = ['RAW', 'HEADER', 'BODY', 'YAML', 'JSON', 'NONE']
    default_format = os.environ.get('OSCURL_FORMAT', 'RAW')

    parser = argparse.ArgumentParser()
    parser.add_argument('request_body_file',
                        nargs='*',
                        help='JSON file which contains a request body')
    parser.add_argument("-s", "--service",
                        help=("service type "
                              "(volume/image/identity/compute/network/...)"
                              ", default=%s" % default_service),
                        default=default_service)
    parser.add_argument("-m", "--method",
                        help=("request method "
                              "(GET/HEAD/POST/PUT/DELETE), "
                              "default=%s" % default_method),
                        choices=supported_methods,
                        default=default_method)
    parser.add_argument("-p", "--path", dest="path",
                        help="differential path of URL",
                        default='')
    parser.add_argument("-P", "--full-path",
                        help="full path of URL")
    parser.add_argument("-f", "--format", dest="format",
                        help=("format of response output "
                              "(RAW/HEADER/BODY/YAML/JSON/NONE), "
                              "default=%s" % default_format),
                        choices=supported_formats,
                        default=default_format)
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="debug mode")
    parser.add_argument("-r", "--dump-request",
                        action="store_true",
                        help="dump HTTP request")
    parser.add_argument("-t", "--api",
                        choices=['public', 'internal', 'admin'],
                        help=("API type (public/internal/admin), "
                              "default=public"))
    parser.add_argument("-z", "--delay",
                        action="store_true",
                        help="test mode, use expired token")

    # Use parse_known_args to show only oscurl options.
    # os_client_config provides a lot of options and
    # it might be annoying for existing oscurl users.
    # Note that all os_client_config options like --os-cloud can be used.
    parser.parse_known_args()

    cloud_config = os_client_config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)
    options = parser.parse_args()

    # os_client_config uses --os-interface option.
    # Map --api option to --os-interface.
    if options.api:
        options.os_interface = options.api

    body = ''
    if options.request_body_file:
        for line in fileinput.input(options.request_body_file):
            body += line.strip()
        json.loads(body)

    do_request(body, cloud_config, options)


if __name__ == '__main__':
    main()
