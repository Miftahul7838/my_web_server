from .http_method import HttpMethod
import subprocess
import subprocess

class HttpPost(HttpMethod):
    """Post data to the server"""
    
    def __init__(self, uri, cont_len, body:dict) -> None:
        """initiates the instance for this class"""
        super().__init__("")
        self.__body = body.strip()
        self.__cont_len = cont_len

    def welcome_user(self) -> str:
        """Posts data from body of the post request
        
        Returns:
        (response code, response body): response code and body based on if
                                        it was able to post the data or not
        """
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
            file_cont = ""
            greet_user = out.split('\n')[-1].strip()
            file_path = "../www/welcome.html"
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Modify the line containing the header
            header_line_index = None
            for i, line in enumerate(lines):
                if '<h1>' in line:
                    header_line_index = i
                    lines[header_line_index] = f'    <h1>{greet_user}</h1>\n'
                    break

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)

            with open(file_path) as file:
                for line in file:
                    file_cont += line
            
            cmd = "cat ../www/welcome.html"
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out = p.stdout.decode()
            err = p.stderr.decode()

            return (200, file_cont.strip())
        except:
            return (500, None)

    
