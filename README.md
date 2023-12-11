<pre>
'''
usage: python3 webserver.py [-h] [--cert CERT] [--key KEY] IP PORT

A http(s) webserver

positional arguments:
  IP           The IP address to start on
  PORT         The port to listen to

options:
  -h, --help   show this help message and exit

Optional argument:
  if you use these options, then both must be used

  --cert CERT  The certificate file
  --key KEY    Corresponding key file of the certificate

Use "python3 ./webserver.py IP PORT --cert example.pem --key example.key" to start the webserver with TLS 
-OR- 
Use "python3 ./webserver.py IP PORT" to start the webser without TLS
'''
</pre>
