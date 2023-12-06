from argparse import ArgumentParser, Namespace, Action
from collections.abc import Sequence
import os
from typing import Any
import ipaddress
from json import loads

class ArgValidation(Action):
    
    def __valid_ip_format(self, ip) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def __ip_reachable(self, ip) -> bool:
        try:
        # Run the ping command and capture the output
            response = os.system(f"ping -c 1 {ip}")  # On Windows, replace '-c' with '-n'
            if response == 0:
                return True  # IP address is reachable
            else:
                return False  # IP address is not reachable
        except Exception:
            return False  # An error occurred, IP address is not reachable
    
    def __valid_ip(self, ip, parser) -> None:
        if self.__valid_ip_format(ip):
            if not self.__ip_reachable(ip):
                parser.error(f"{ip} is not reachable!")
            else:
                return ip
        else:
            parser.error(f"{ip} not valid IP format")      

    def __valid_port_range(self, port, parser) -> bool:
        port = int(port)
        if port == 80 or port == 443:
            return port
        elif 1024 <= port <= 65535:
            return port
        parser.error(f"{port} is not in port range")

    def __read_http_request_file(self, filename:str) -> str:
        req_str = ""
        with open(filename,'r') as file:
            for line in file:
                req_str += line
        return req_str
    
    def __has_one_http_req(self, filename, parser) -> None:
        """Checks the file for one HTTP request

        Args:
        filename: the file that contains HTTP request
        """
        has_one_methods = False
        http_req_str = ""
        methods = os.environ.get("HTTP_METHODS")
        methods = methods.replace("'", '"')
        allowed_methods = loads(methods)
        with open(filename, 'r') as file:
            for line in file:
                if line.split(" ")[0] in allowed_methods.keys():
                    if not has_one_methods:
                        has_one_methods = True
                    else:
                        parser.error(f"{filename} contains two http requests")
        with open(filename,'r') as file:
            http_req_str = file.read()
        return http_req_str

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: str | Sequence[Any] | None, option_string: str | None = None) -> None:
        
        the_option = self.dest
        option_value = values
        validated_arg = None

        match the_option:
            case "ip_address":
                validated_arg = self.__valid_ip(option_value, parser)
            case "port":
                validated_arg = self.__valid_port_range(option_value, parser)
            case "http_req":
                validated_arg = self.__has_one_http_req(option_value.name, parser)

        setattr(namespace, self.dest, validated_arg)

        


            