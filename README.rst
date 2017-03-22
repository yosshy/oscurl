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

Output Format
-------------

* RAW: Both HTTP response headers and body (Default)::

   $ oscurl -p /servers
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-f2c0adc9-288b-4a65-8243-b112d1dc60b6
   Content-Type: application/json
   Content-Length: 366
   Date: Sun, 22 Jun 2014 12:25:16 GMT

   {"servers": [{"id": "fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "links": [{"href": "http://192.168.0.11:8774/v2/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "self"}, {"href": "http://192.168.0.11:8774/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "bookmark"}], "name": "server-test-1"}]}

* HEADER: Only HTTP response headers::

   $ oscurl -p /servers -f HEADER
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-f2c0adc9-288b-4a65-8243-b112d1dc60b6
   Content-Type: application/json
   Content-Length: 366
   Date: Sun, 22 Jun 2014 12:25:16 GMT


* BODY: Only HTTP response body::

   $ oscurl -p /servers -f BODY
   {"servers": [{"id": "fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "links": [{"href": "http://192.168.0.11:8774/v2/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "self"}, {"href": "http://192.168.0.11:8774/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "bookmark"}], "name": "server-test-1"}]}

* JSON: Human-readable JSON format::

   $ oscurl -p /servers -f JSON
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-cf070813-5259-4b83-86bd-e4e2c6d31d1f
   Content-Type: application/json
   Content-Length: 366
   Date: Sun, 22 Jun 2014 12:27:38 GMT

   {
     "servers": [
       {
         "id": "fdec5b9e-9b6a-4eb4-8684-6c75cd275559",
         "links": [
           {
             "href": "http://192.168.0.11:8774/v2/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559",
             "rel": "self"
           },
           {
             "href": "http://192.168.0.11:8774/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559",
             "rel": "bookmark"
           }
         ],
         "name": "server-test-1"
       }
     ]
   }

* YAML: HTTP response body in YAML::

   $ oscurl -p /servers -f YAML
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-14638074-8093-42d1-b872-5a4e6a5ebb6a
   Content-Type: application/json
   Content-Length: 366
   Date: Sun, 22 Jun 2014 12:29:30 GMT

   servers:
   - id: fdec5b9e-9b6a-4eb4-8684-6c75cd275559
     links:
     - {href: 'http://192.168.0.11:8774/v2/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559',
       rel: self}
     - {href: 'http://192.168.0.11:8774/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559',
       rel: bookmark}
     name: server-test-1

* ``-r``: With HTTP request::

   $ oscurl -p /servers -r
   ==== HTTP REQUEST ====
   GET /v2/d046e2315c27456b9eb26740a9e39143/servers HTTP/1.1
   Host: 192.168.0.11:8774
   Accept-Encoding: identity
   Content-Type: application/json
   Accept: application/json
   X-Auth-Token: MIIKswYJKoZ...KZ1BBJg==


   ==== HTTP RESPONSE ====
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-85955345-f8c4-41e9-859c-c20b5b1355f6
   Content-Type: application/json
   Content-Length: 366
   Date: Sun, 22 Jun 2014 12:31:31 GMT

   {"servers": [{"id": "fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "links": [{"href": "http://192.168.0.11:8774/v2/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "self"}, {"href": "http://192.168.0.11:8774/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "bookmark"}], "name": "server-test-1"}]}

