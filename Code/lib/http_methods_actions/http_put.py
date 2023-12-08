import subprocess
from .http_method import HttpMethod
import os
from json import loads

class HttPPut(HttpMethod):

    def __init__(self, uri, data) -> None:
        super().__init__(uri)
        self.__data = data
        if "\n" in self.__data:
            self.__data = self.__data.split('\n')
        if self.__data == None:
            self.__data = ""
        self.__web_root =  loads(str(os.environ.get('WEB_ROOT').replace("'",'"'))).get('web_root')

    def insert_data(self):
        file_exists = self.file_exists_in_webroot()
        ret_code = file_exists[0]
        ful_path = file_exists[1]
        file_location = ""
        try:
            if ret_code == 200:
                file_location = ful_path
                with open(file_location,'rw') as file:
                    for line in self.__data:
                        file.writelines(line+"\n")
            else:
                file_location = ful_path + self.__web_root + '/' + self.uri
                os.system("touch " + file)
                with open(file,'rw') as f:
                    for line in self.__data:
                        f.writelines(line+"\n")

            return (201, ful_path)
        except:
            return (500, None)
        
            

    