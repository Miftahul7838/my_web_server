from .http_request_parser.http_parse_startline import HttpParseStartLine as HPS
from .http_request_parser.http_parse_field import HttpParseField as HPF
from .http_request_parser.http_parse_body import HttpParseBody as HPB

class HttpClientRequst:
    HTTP_METHODS = None

    def __init__(self, http_request:str) -> None:
        self.__req_str = http_request
        self.__start_line = ""
        self.__field_line = ""
        self.__body_line = ""
        self.__has_body = False
        self.__LF = "\n"

        if self.__LF in self.__req_str:
            self.__req_str = self.__req_str.split(self.__LF)
            req_len = len(self.__req_str)
            #setting lines
            if req_len >= 2:
                # setting start line
                self.__start_line  = self.__req_str[0]
                # setting field line
                for i in range(1,req_len):
                    if self.__req_str[i] == '':
                        break
                    self.__field_line += self.__req_str[i] + "\n"
                # if there is a body, then then the body field is set as well
                body_start_index = self.__req_str.index('')
                for i in range(body_start_index, req_len):
                    self.__body_line += self.__req_str[i] + '\n'
                self.__len_body_line = len(self.__body_line.split())
                if self.__len_body_line != 0:
                    self.__has_body = True

    def is_valid_req(self) -> tuple:
        ret_code = None
        try:
            start_line = HPS(self.__start_line)
            valid_start_line = start_line.is_valid_start_line()
            ret_code = valid_start_line[0]
            if ret_code == 200:
                method = valid_start_line[1][0]
                field_line = HPF(self.__field_line, method)
                valid_field_line = field_line.is_valid_field_line()
                ret_code = valid_field_line[0]
                fields = valid_field_line[1]
                if ret_code == 200:
                    if self.__has_body:
                        con_len = fields.get("content-length")
                        # Parsing the body and checking for syntax error
                        body_line = HPB(self.__body_line, con_len, method)
                        valid_body_line = body_line.is_valid_body()
                        ret_code = valid_body_line[0]
                        if ret_code == 200:
                            return (ret_code, valid_start_line[1], fields, valid_body_line[1])
                        else:
                            (ret_code, None, None, None)
                    else:
                        return (ret_code, valid_start_line[1], fields, None)
                else:
                    return (ret_code, valid_start_line[1], None, None)
            else:
                return (ret_code, None, None, None)
        except:
            return (500, None, None, None)
            

        

        

