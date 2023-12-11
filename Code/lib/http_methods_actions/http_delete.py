from .http_method import HttpMethod
import subprocess
import os

class HttpDelete(HttpMethod):

    def __init__(self, uri) -> None:
        super().__init__(uri)
        self.__file_exists = self.file_exists_in_webroot()
        self.__ret_code = self.__file_exists[0]
        self.__file_path = self.__file_exists[1]

    def delete_file(self) -> tuple:
        if self.__ret_code == 200:
            cmd = "rm -f " + self.__file_path
            p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            err = p.stderr.decode()
            out = p.stdout.decode()
            return (200, "file has been deleted")
        else:
            return (404, None)

            

