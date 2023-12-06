import subprocess
from json import loads
import os

class HttpMethod:

    def __init__(self, uri) -> None:
        self.uri = uri
        if uri != "":
            if '/' in uri:
                self.file = uri.split('/')
            else:
                self.file = uri
            self.__len_file = len(self.file)
            self.req_file = self.file[self.__len_file - 1]
            self.__web_root = loads(str(os.environ.get('WEB_ROOT').replace("'",'"'))).get('web_root')

    def __get_web_root_path(self) -> str:
        file_path = ""
        cmd = "pwd"
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out = p.stdout.decode().replace('\n', '/')
        path_dir_list = out.split('/')
        for dir in path_dir_list:
            file_path += dir + '/'
            if dir == "Code":
                break
        return file_path

    def file_exists_in_webroot(self) -> tuple:
        file_path = self.__get_web_root_path()
        absolute_file_path = file_path + self.__web_root + '/'
        cmd = f'find {absolute_file_path} -name "{self.req_file}" | grep -e "{self.req_file}"'
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = p.stdout.decode()
        err = p.stderr.decode()
        if err == "" and out != "":
            if "/" in out:
                diced_path = out.strip().split('/')
                if self.req_file in diced_path:
                    return (200, out.strip())
        return (404, file_path)


