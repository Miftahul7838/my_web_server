Contains all the custome libraries that are essential to this webserver:

Files:
http_client_req.py: parse the http request and returns response code and body specific to the type of request
http_server_resp.py: accoding to the response code and body it return a response that the server should return 
argvalidation.py: is used to validate argument for terminal based tools like the webserver.py and httpReq.py

Directories:
http_request_parser: has files to parse startline, fieldline, and bodyline
http_method_action: has files for each HTTP methods that are supported and are parsed