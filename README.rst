oscurl
======

**oscurl** is a tool to access OpenStack APIs as raw. You can specify method,
URL path and body of HTTP requests freely. It's useful to test, check or
confirm OpenStack APIs.

You don't need to handle Keystone authentication; **oscurl** does it
automatically with OpenStack credentials.

**oscurl** supports multiple ways to specify keystone credentials:

* Legacy way to use ``OS_*`` environment variables
* os-client-config via ``OS_CLOUD`` environment variable

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

Examples
--------

* Get server list::

  $ oscurl -p /servers

* Get flavor list::

  $ oscurl -p /flavors

* Get image list from Nova::

  $ oscurl -p /images

* Get image list from Glance::

  $ oscurl -s image -p /images

* Get volume list from Nova::

  $ oscurl -p /os-volumes

* Get volume snapshot list from Nova::

  $ oscurl -p /os-snapshots

* Get volume list from Cinder::

  $ oscurl -s volume -p /volumes

* Get volume list from Cinder::

  $ oscurl -s volume -p /snapshots

* Get network list from Nova::

   $  oscurl -p /os-networks

* Get network list from Neutron::

   $ oscurl -s network -p /v2.0/networks

* Get subnet list::

   $ oscurl -s network -p /v2.0/subnets

* Get network port list::

   $ oscurl -s network -p /v2.0/ports

* Create a new instance::

   $ cat create_instance_body
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
   $ oscurl -m POST -p /servers create_instance_body

  or::

   $ oscurl -m POST -p /servers - < create_instance_body

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

* -r: With HTTP request::

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

