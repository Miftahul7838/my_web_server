from .http_method import HttpMethod
from datetime import datetime

class HttpHead(HttpMethod):

    def __init__(self, uri) -> None:
        super().__init__(uri)
        self.__file_exists = self.file_exists_in_webroot()
        self.__ret_code = self.__file_exists[0]

    def get_file_head(self) -> tuple:
        file_cont = ""
        out = ""
        if self.__ret_code == 200:
            file_path = self.__file_exists[1]
            with open(file_path) as file:
                for line in file:
                    file_cont += line
            
            file_location = "location: " + file_path
            out += file_location + '\n'
            out += "content-length: " + str(len(file_cont)) + '\n'
            out += "date: " + str(datetime.now().strftime("%A, %B %d, %Y")) + '\n'
            
            return (200, out)
        else:
            
            return (404, None)

            

