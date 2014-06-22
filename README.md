======
oscurl
======

oscurl is a tool to access OpenStack APIs as raw. It's useful to test/check/confirm them.

Install
=======

1. Download oscurl.
   ```
   $ git clone https://github.com/yosshy/oscurl.git
   ```

2. Make it executable.
   ```
   $ chmod +x oscurl/oscurl
   ```

3. Copy oscurl file under the execution path.
   ```
   $ sudo cp oscurl/oscurl /usr/local/bin
   ```

4. Test oscurl.
   ```
   $ oscurl -h
   Usage: oscurl [options]

   Options:
     -h, --help            show this help message and exit
     -s SERVICE, --service=SERVICE
                           service name or type, default=compute
     -m METHOD, --method=METHOD
                           request method (POST/GET/DELETE/...), default=GET
     -p PATH, --path=PATH  differential path of URL
     -P FULLPATH, --full-path=FULLPATH
                           full path of URL
     -f FORMAT, --format=FORMAT
                           type of response
                           output(RAW|HEADER|BODY|YAML|JSON|NONE), default=RAW
     -d, --debug           debug mode
     -r, --dump-request    dump HTTP request
     ```

Usage
=====

1. Set environment variables as same as you use nova command.
   ```
   $ source credential_file
   ```

2. Run oscurl.
   ```
   $ oscurl -p /servers
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-e5d6537e-9db8-48a2-abfb-f3a63f17add5
   Content-Type: application/json
   Content-Length: 15
   Date: Sun, 22 Jun 2014 12:20:46 GMT
   
   {"servers": []}
   ```

Output Formats
==============

* RAW: Both HTTP response headers and body (Default)
   ```
   $ oscurl -p /servers
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-f2c0adc9-288b-4a65-8243-b112d1dc60b6
   Content-Type: application/json
   Content-Length: 366
   Date: Sun, 22 Jun 2014 12:25:16 GMT
   
   {"servers": [{"id": "fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "links": [{"href": "http://192.168.0.11:8774/v2/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "self"}, {"href": "http://192.168.0.11:8774/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "bookmark"}], "name": "server-test-1"}]}
   ```

* HEADER: Only HTTP response headers
   ```
   $ oscurl -p /servers
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-f2c0adc9-288b-4a65-8243-b112d1dc60b6
   Content-Type: application/json
   Content-Length: 366
   Date: Sun, 22 Jun 2014 12:25:16 GMT

   ```

* BODY: Only HTTP response body
   ```
   $ oscurl -p /servers
   {"servers": [{"id": "fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "links": [{"href": "http://192.168.0.11:8774/v2/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "self"}, {"href": "http://192.168.0.11:8774/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "bookmark"}], "name": "server-test-1"}]}
   ```

* JSON: Human-readable JSON format
   ```
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
   ```

* YAML: HTTP response body in YAML
   ```
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
   ```

* -r: With HTTP request
   ```
   $ oscurl -p /servers -r
   ==== HTTP REQUEST ====
   GET /v2/d046e2315c27456b9eb26740a9e39143/servers HTTP/1.1
   Host: 192.168.0.11:8774
   Accept-Encoding: identity
   Content-Type: application/json
   Accept: application/json
   X-Auth-Token: MIIKswYJKoZIhvcNAQcCoIIKpDCCCqACAQExCTAHBgUrDgMCGjCCCYwGCSqGSIb3DQEHAaCCCX0Eggl5eyJhY2Nlc3MiOiB7InRva2VuIjogeyJpc3N1ZWRfYXQiOiAiMjAxNC0wNi0yMlQxMjozMTozMC44OTE1NDMiLCAiZXhwaXJlcyI6ICIyMDE0LTA2LTIzVDEyOjMxOjMwWiIsICJpZCI6ICJwbGFjZWhvbGRlciIsICJ0ZW5hbnQiOiB7ImRlc2NyaXB0aW9uIjogbnVsbCwgImVuYWJsZWQiOiB0cnVlLCAiaWQiOiAiZDA0NmUyMzE1YzI3NDU2YjllYjI2NzQwYTllMzkxNDMiLCAibmFtZSI6ICJwcm9qZWN0X29uZSJ9fSwgInNlcnZpY2VDYXRhbG9nIjogW3siZW5kcG9pbnRzIjogW3siYWRtaW5VUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo4Nzc0L3YyL2QwNDZlMjMxNWMyNzQ1NmI5ZWIyNjc0MGE5ZTM5MTQzIiwgInJlZ2lvbiI6ICJSZWdpb25PbmUiLCAiaW50ZXJuYWxVUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo4Nzc0L3YyL2QwNDZlMjMxNWMyNzQ1NmI5ZWIyNjc0MGE5ZTM5MTQzIiwgImlkIjogIjQxODliMDVhOWIzMDQwZTVhMGU3ZTdkNTA0MGJlMjQ3IiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTkyLjE2OC4wLjExOjg3NzQvdjIvZDA0NmUyMzE1YzI3NDU2YjllYjI2NzQwYTllMzkxNDMifV0sICJlbmRwb2ludHNfbGlua3MiOiBbXSwgInR5cGUiOiAiY29tcHV0ZSIsICJuYW1lIjogIm5vdmEifSwgeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vMTkyLjE2OC4wLjExOjk2OTYvIiwgInJlZ2lvbiI6ICJSZWdpb25PbmUiLCAiaW50ZXJuYWxVUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo5Njk2LyIsICJpZCI6ICIzNjU2ZmY5MDQyMDU0MzY3YTM1ZDI2MzBjZmJjMDBjYiIsICJwdWJsaWNVUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo5Njk2LyJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJuZXR3b3JrIiwgIm5hbWUiOiAicXVhbnR1bSJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly8xOTIuMTY4LjAuMTE6OTI5Mi92MiIsICJyZWdpb24iOiAiUmVnaW9uT25lIiwgImludGVybmFsVVJMIjogImh0dHA6Ly8xOTIuMTY4LjAuMTE6OTI5Mi92MiIsICJpZCI6ICIyZTI5N2JiYjY1ZmE0MmYzYTQzOWY0M2IzMDhiZjQxYiIsICJwdWJsaWNVUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo5MjkyL3YyIn1dLCAiZW5kcG9pbnRzX2xpbmtzIjogW10sICJ0eXBlIjogImltYWdlIiwgIm5hbWUiOiAiZ2xhbmNlIn0sIHsiZW5kcG9pbnRzIjogW3siYWRtaW5VUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo4Nzc2L3YxL2QwNDZlMjMxNWMyNzQ1NmI5ZWIyNjc0MGE5ZTM5MTQzIiwgInJlZ2lvbiI6ICJSZWdpb25PbmUiLCAiaW50ZXJuYWxVUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo4Nzc2L3YxL2QwNDZlMjMxNWMyNzQ1NmI5ZWIyNjc0MGE5ZTM5MTQzIiwgImlkIjogIjExNGRmY2MxZWQ5MDQ1MThhNGI4NjlkZDM3MjZjNDI3IiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTkyLjE2OC4wLjExOjg3NzYvdjEvZDA0NmUyMzE1YzI3NDU2YjllYjI2NzQwYTllMzkxNDMifV0sICJlbmRwb2ludHNfbGlua3MiOiBbXSwgInR5cGUiOiAidm9sdW1lIiwgIm5hbWUiOiAiY2luZGVyIn0sIHsiZW5kcG9pbnRzIjogW3siYWRtaW5VUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo4NzczL3NlcnZpY2VzL0FkbWluIiwgInJlZ2lvbiI6ICJSZWdpb25PbmUiLCAiaW50ZXJuYWxVUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo4NzczL3NlcnZpY2VzL0Nsb3VkIiwgImlkIjogIjE0OWQ5ZGJkZWJiNTQwNTY4YWVhYzc2ZmIxNDZlODYyIiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTkyLjE2OC4wLjExOjg3NzMvc2VydmljZXMvQ2xvdWQifV0sICJlbmRwb2ludHNfbGlua3MiOiBbXSwgInR5cGUiOiAiZWMyIiwgIm5hbWUiOiAiZWMyIn0sIHsiZW5kcG9pbnRzIjogW3siYWRtaW5VUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTozNTM1Ny92Mi4wIiwgInJlZ2lvbiI6ICJSZWdpb25PbmUiLCAiaW50ZXJuYWxVUkwiOiAiaHR0cDovLzE5Mi4xNjguMC4xMTo1MDAwL3YyLjAiLCAiaWQiOiAiMjhjNzMzNjQxYTAxNDU2ZWEzNTI2YjQzYTdkODU3MDAiLCAicHVibGljVVJMIjogImh0dHA6Ly8xOTIuMTY4LjAuMTE6NTAwMC92Mi4wIn1dLCAiZW5kcG9pbnRzX2xpbmtzIjogW10sICJ0eXBlIjogImlkZW50aXR5IiwgIm5hbWUiOiAia2V5c3RvbmUifV0sICJ1c2VyIjogeyJ1c2VybmFtZSI6ICJ1c2VyX29uZSIsICJyb2xlc19saW5rcyI6IFtdLCAiaWQiOiAiOTMzNDE1YTIxNjc1NGM2Nzk0MDM2MjY2OTU5NjkyNTYiLCAicm9sZXMiOiBbeyJuYW1lIjogIl9tZW1iZXJfIn0sIHsibmFtZSI6ICJhZG1pbiJ9XSwgIm5hbWUiOiAidXNlcl9vbmUifSwgIm1ldGFkYXRhIjogeyJpc19hZG1pbiI6IDAsICJyb2xlcyI6IFsiOWZlMmZmOWVlNDM4NGIxODk0YTkwODc4ZDNlOTJiYWIiLCAiMTc0OTYyYjU4MDc4NDA3Zjk1NTAzOTI5YjA2NmMzOGMiXX19fTGB-zCB-AIBATBcMFcxCzAJBgNVBAYTAlVTMQ4wDAYDVQQIEwVVbnNldDEOMAwGA1UEBxMFVW5zZXQxDjAMBgNVBAoTBVVuc2V0MRgwFgYDVQQDEw93d3cuZXhhbXBsZS5jb20CAQEwBwYFKw4DAhowDQYJKoZIhvcNAQEBBQAEgYCLIhw9v+DfXF76DYQ8oa-ZODOYDRV4Mg01rEcpDC7kh7ape--9pa7qvnclm1oyhiiTjl1Ouc+47elHIdn05z7RHPo6+AxVQu1PcIP99gXyQNFG-wUWbZDoOPxLvhJgEeRzlJVrtzmj4coAiecNvab4GRhjNnQ-8mwYOzNKZ1BBJg==
   
   
   ==== HTTP RESPONSE ====
   HTTP/1.1 200 OK
   X-Compute-Request-Id: req-85955345-f8c4-41e9-859c-c20b5b1355f6
   Content-Type: application/json
   Content-Length: 366
   Date: Sun, 22 Jun 2014 12:31:31 GMT
   
   {"servers": [{"id": "fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "links": [{"href": "http://192.168.0.11:8774/v2/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "self"}, {"href": "http://192.168.0.11:8774/d046e2315c27456b9eb26740a9e39143/servers/fdec5b9e-9b6a-4eb4-8684-6c75cd275559", "rel": "bookmark"}], "name": "server-test-1"}]}
   ```

Examples
========

* Get server list:
  ```
  $ oscurl -p /servers
  ```

* Get flavor list:
  ```
  $ oscurl -p /flavors
  ```

* Get image list from Nova:
  ```
  $ oscurl -p /images
  ```

* Get image list from Glance:
  ```
  $ oscurl -s image -p /images
  ```

* Get volume list from Nova:
  ```
  $ oscurl -p /os-volumes
  ```

* Get volume snapshot list from Nova:
  ```
  $ oscurl -p /os-snapshots
  ```

* Get volume list from Cinder:
  ```
  $ oscurl -s volume -p /volumes
  ```

* Get volume list from Cinder:
  ```
  $ oscurl -s volume -p /snapshots
  ```

* Get network list from Nova:
   ```
   $  oscurl -p /os-networks
   ```

* Get network list from Neutron:
   ```
   $ oscurl -s network -p /v2.0/networks
   ```

* Get subnet list:
   ```
   $ oscurl -s network -p /v2.0/subnets
   ```

* Get network port list:
   ```
   $ oscurl -s network -p /v2.0/ports
   ```
