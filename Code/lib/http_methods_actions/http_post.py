from .http_method import HttpMethod
import subprocess
import subprocess
import os

class HttpPost(HttpMethod):
    
    def __init__(self, uri, cont_len, body:dict) -> None:
        super().__init__("")
        self.__body = body.strip()
        self.__cont_len = cont_len

    def welcome_user(self) -> str:
        cmd = (
            'export GATEWAY_INTERFACE="CGI/1.1";'
            'export SCRIPT_FILENAME="./postname.php";'
            'export REQUEST_METHOD="POST";'
            'export SERVER_PROTOCOL="HTTP/1.1";'
            'export REMOTE_HOST="127.0.0.1";'
            f'export CONTENT_LENGTH={self.__cont_len};'
            f'export BODY="{self.__body}";'
            'export CONTENT_TYPE="application/x-www-form-urlencoded";'
            'export REDIRECT_STATUS=200;'
            'echo "$BODY" | php-cgi'
        )

        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = p.stdout.decode()
        err = p.stderr.decode()
        try:
            greet_user = out.split('\n')[-1].strip()
            return (200, greet_user)
        except:
            return (500, None)

    
