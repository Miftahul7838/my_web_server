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

    def insert_data(self):
        file_exists = self.file_exists_in_webroot()
        ret_code = file_exists[0]
        ful_path = file_exists[1]
        if ret_code == 200:
            with open(ful_path,'rw') as file:
                for line in self.__data:
                    file.writelines(line+"\n")
        else:
            pass

    