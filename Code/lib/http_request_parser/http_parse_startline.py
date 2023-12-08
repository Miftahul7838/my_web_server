import re
import os
from json import loads

class HttpParseStartLine:

    def __init__(self, start_line) -> None:
        self.__start_line = start_line
        # Getting allowed methods from environment variable
        self.__tmp_methods = os.environ.get('HTTP_METHODS')
        self.__tmp_methods = self.__tmp_methods.replace("'", '"')
        self.__methods = loads(self.__tmp_methods)
        # getting the web root
        self.__web_path = os.environ.get('WEB_ROOT')
        self.__tmp_path = self.__web_path.replace("'", '"')
        if "BSL" not in self.__tmp_path:
            self.__allowed_paths = loads(self.__tmp_path).get("allowed_path").split(',')
        else:
            self.__allowed_paths = loads(self.__tmp_path).get("allowed_path").replace('BSL',"\\").split(',')
        self.__allowed_paths = list(map(str.strip, self.__allowed_paths))

        self.__start_line = self.__start_line.split()
        self.__start_line_len = len(self.__start_line)
        if self.__start_line_len == 3:
            self.__method = self.__start_line[0]
            self.__path = self.__start_line[1]
            self.__http_verion = self.__start_line[2]
        else:
            return 400

    def __is_valid_method(self, method:str) -> bool:
        method = method.upper()
        methods_list = self.__methods.keys()
        if method in methods_list:
            is_supp = self.__methods.get(method).get("supported")
            if is_supp == 'yes':
                return True
        return False

    def __is_valid_http_req_path(self, uri:str) -> bool:
        """Checks if the URI is valid according to RFC 9110.

        Args:
            uri: A string representing the URI.
                     
        Returns:
            is_valid: True if the URI is valid, False otherwise.
        """
        match_found = any(re.match(pattern, uri) for pattern in self.__allowed_paths)
        if uri.startswith('/'):
            if uri == '/' or match_found:
                return True
        return False

    def __is_valid_http_version(self, http_version:str) -> bool:
        """Checks the http request http version

        Args:
        http_version: the version of the http

        Returns:
        is_valid: Either True or False depending on if the version is supported or not, and
        if it is in valid format
        """
        is_valid = False
        match = re.match(r'^HTTP/(\d+\.\d+)$', http_version)
        if match:
            http_version = http_version.split("/")[1].split(".")
            if int(http_version[0]) == 1:
                if int(http_version[1]) >= 0 or http_version[1] <= 3:
                    return True
        return False

    def is_valid_start_line(self) -> tuple:
        """Checks the start line of the http request for valid format

        Args:
        starline: the startline of the http request

        Returns:
        start_line_info: is a tuple that contains either True or False
                        as its first value and and a dictionary or None
                        depending on if the start_line_info is valid or not
        """
        resp_codes = []
        valid_method = self.__is_valid_method(self.__method)
        valid_path = self.__is_valid_http_req_path(self.__path)
        valid_http_version = self.__is_valid_http_version(self.__http_verion)

        if not valid_method:
            resp_codes.append(501)
        elif not valid_path:
            resp_codes.append(403)
        elif not valid_http_version:
            resp_codes.append(505)
        else:
            resp_codes.append(200)
        
        is_valid = resp_codes[0]
        if is_valid == 200:
            if self.__path == "/":
                self.__path = "/index.html"
            return (is_valid, (self.__method, self.__path, self.__http_verion))
        return (is_valid, None)
