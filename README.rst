oscurl
======

**oscurl** is a tool to access OpenStack APIs as raw. You can specify method,
URL path and body of HTTP requests freely. It's useful to test, check or
confirm OpenStack APIs.

Features
--------

* cURL-like access to OpenStack APIs
* Handle Keystone authentication and insert ``X-Auth-Token`` header;
  You do not need to handle Keystone authentication manually
* Construct URL based on OpenStack service endpoints (relative mode)
* Support multiple output formats: raw, YAML, JSON, header only and body only
* Show request header and body
* Keystone v3 and v2 support
* Microversioning header support. 'latest' is used by default.
* Support multiple ways to specify keystone credentials:

  * Legacy way to use ``OS_*`` environment variables
  * os-client-config via ``OS_CLOUD`` environment variable

* JSON input for ``POST`` and ``PUT`` requests

Installation
------------

oscurl is available at PyPI (the Python Packaging Index).
To install oscurl, just run::

    $ pip install oscurl

Usage
-----

1. Set environment variables as same as you use nova command::

       $ source credential_file

   or if you have os-client-config configuration like /etc/openstack/clouds.yaml::

       $ export OS_CLOUD=<env-name>

2. Run oscurl::

       $ oscurl -p /servers
       HTTP/1.1 200 OK
       X-Compute-Request-Id: req-e5d6537e-9db8-48a2-abfb-f3a63f17add5
       Content-Type: application/json
       Content-Length: 15
       Date: Sun, 22 Jun 2014 12:20:46 GMT

       {"servers": []}

3. ``oscurl --help`` shows the options.
   ``oscurl --full-help`` shows the options from os-client-config too.

Environment Variables
---------------------

The following environment variables can be used
to change the default behavior.

* ``OSCURL_SERVICE``: the default service type.
  Service types registered in Keystone service catalog like
  like ``compute``, ``volume``, ``identity``, ``image`` and ``network``
* ``OSCURL_FORMAT``: the default format used to display API responses
* ``OSCURL_METHOD``: the default method to be used

Examples
--------

* Get server list from Nova::

  $ oscurl -p /servers

* Get flavor list from Nova::

  $ oscurl -p /flavors

* Get image list from Glance::

  $ oscurl -s image -p /images

* Get volume list from Cinder::

  $ oscurl -s volume -p /volumes

* Get network list from Neutron::

   $ oscurl -s network -p /v2.0/networks

* Create a new instance by passing the input as JSON file::

   $ oscurl -m POST -p /servers -i create_instance_body.json

  or::

   $ oscurl -m POST -p /servers -i - < create_instance_body.json

  The content of ``create_instance_body.json`` is like below::

   {
       "server": {
           "name": "server-test-1",
           "imageRef": "19befdd4-248b-4b8d-b586-8a91a8bf8623",
           "flavorRef": "1",
           "max_count": 1,
           "min_count": 1,
           "networks": [
               {
                   "uuid": "6a2c033b-3f50-4f43-97fa-2517ccdc28d9"
               }
           ],
           "security_groups": [
               {
                   "name": "default"
               }
           ]
       }
   }

* Show an instance information::

   $ oscurl -p /servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559

* Delete an instance::

   $ oscurl -p /servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559 -m DELETE

Output mode
-----------

``--show-mode`` controls what are shown.

* ``ALL`` shows request and response including both headers and body.
* ``RESP`` shows response headers and body. Request headers and body
  are not shown.
* ``BODY`` shows response body only. Useful if you pass output
  to another program like ``jq``.

Output Format
-------------

``--format`` controls the output format of response body.

* ``RAW``: Show response body as-is (Default)::

   $ oscurl -p /servers -r RESP
   HTTP/1.1 200 OK
   Content-Length: 296
   Content-Type: application/json
   Openstack-Api-Version: compute 2.42
   X-Openstack-Nova-Api-Version: 2.42
   Vary: OpenStack-API-Version, X-OpenStack-Nova-API-Version
   X-Compute-Request-Id: req-565bb028-c144-40cc-8fb5-52f1c5ff3b58
   Date: Fri, 24 Mar 2017 09:07:08 GMT
   Connection: keep-alive

   {"servers": [{"id": "2820fcfc-3cd2-4a40-8c01-3c9544cfbc59", "links": [{"href": "http://172.27.201.206:8774/v2.1/servers/2820fcfc-3cd2-4a40-8c01-3c9544cfbc59", "rel": "self"}, {"href": "http://172.27.201.206:8774/servers/2820fcfc-3cd2-4a40-8c01-3c9544cfbc59", "rel": "bookmark"}], "name": "vm1"}]}

* ``JSON``: Human-readable JSON format::

   $ oscurl -p /servers --show-mode RESP -f JSON
   HTTP/1.1 200 OK
   Content-Length: 296
   Content-Type: application/json
   Openstack-Api-Version: compute 2.42
   X-Openstack-Nova-Api-Version: 2.42
   Vary: OpenStack-API-Version, X-OpenStack-Nova-API-Version
   X-Compute-Request-Id: req-3293cc26-c336-454a-b361-0a97aaa8c571
   Date: Fri, 24 Mar 2017 09:09:14 GMT
   Connection: keep-alive

   {
     "servers": [
       {
         "id": "2820fcfc-3cd2-4a40-8c01-3c9544cfbc59", 
         "links": [
           {
             "href": "http://172.27.201.206:8774/v2.1/servers/2820fcfc-3cd2-4a40-8c01-3c9544cfbc59", 
             "rel": "self"
           }, 
           {
             "href": "http://172.27.201.206:8774/servers/2820fcfc-3cd2-4a40-8c01-3c9544cfbc59", 
             "rel": "bookmark"
           }
         ], 
         "name": "vm1"
       }
     ]
   }

* ``YAML``: HTTP response body in YAML::

   $ oscurl -p /servers --show-mode RESP -f YAML
   HTTP/1.1 200 OK
   Content-Length: 296
   Content-Type: application/json
   Openstack-Api-Version: compute 2.42
   X-Openstack-Nova-Api-Version: 2.42
   Vary: OpenStack-API-Version, X-OpenStack-Nova-API-Version
   X-Compute-Request-Id: req-69d39243-cd55-4ee8-a6cf-9eb7a7e94fad
   Date: Fri, 24 Mar 2017 09:11:18 GMT
   Connection: keep-alive

   servers:
   - id: 2820fcfc-3cd2-4a40-8c01-3c9544cfbc59
     links:
     - {href: 'http://172.27.201.206:8774/v2.1/servers/2820fcfc-3cd2-4a40-8c01-3c9544cfbc59',
       rel: self}
     - {href: 'http://172.27.201.206:8774/servers/2820fcfc-3cd2-4a40-8c01-3c9544cfbc59',
       rel: bookmark}
     name: vm1

