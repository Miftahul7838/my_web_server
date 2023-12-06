from .http_method import HttpMethod
import subprocess

class HttpGet(HttpMethod):

    def __init__(self, uri) -> None:
        super().__init__(uri)
        self.__file_exists = self.file_exists_in_webroot()
        self.__ret_code = self.__file_exists[0]

    def get_file_cont(self) -> tuple:
        file_cont = ""
        if self.__ret_code == 200:
            file_path = self.__file_exists[1]
            with open(file_path) as file:
                for line in file:
                    file_cont += line
            return (200, file_cont)
        else:
            cmd = f'php-cgi ../src/'+self.req_file.replace('?'," ")
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out = p.stdout.decode()
            err = p.stderr.decode()
            if out != "File not found":
                return (200, out)
            return (404, out)

            

