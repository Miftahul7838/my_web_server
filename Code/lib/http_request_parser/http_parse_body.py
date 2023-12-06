import os
from json import loads

class HttpParseBody:

    def __init__(self, body, cont_len, method) -> None:
        self.__body = body
        self.__cont_len = int(cont_len)
        self.__method = method
        # loading allowed methods from environment variable
        self.__tmp_methods = os.environ.get('HTTP_METHODS')
        self.__tmp_methods = self.__tmp_methods.replace("'", '"')
        self.__allowed_methods = loads(self.__tmp_methods)

    def __should_have_body(self) -> bool:
        has_body = self.__allowed_methods.get(self.__method.upper()).get('has_body')
        if has_body == 'yes':
            return True
        return False

    def __valid_data(self) -> bool:
        body_str = ""
        try:
            for i in range(self.__cont_len):
                body_str += self.__body[i]
            return 200
        except:
            return 400
        
    def is_valid_body(self) -> bool:
        if self.__should_have_body():
            valid_len = self.__valid_data()
            if valid_len:
                return (200, self.__body)
            return (400, None)
        else:
            return (400, None)