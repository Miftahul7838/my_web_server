contains the config file for the webserver

path (contains the web root and allowed path):
    web_root: is where the directory for the frontend or files that are public
    allowed_path: all the paths that are allowed by the webserver
        - you can append a path with a "/" followed by the path
            - the path following "/" can also be a python regex
                - if using regex, then note that "BSL" is parsed as backslash or "\"
    
http_methods (all the methdos that are allowed):
    {METHOD}:
        supported: (yes/no) - if the method is supported or not
        body: (yes/no) - if the method has body or not