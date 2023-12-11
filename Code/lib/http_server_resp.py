class HttpServerResponse:
    """Server response"""


    STATUS_CODE = {200:"OK", 201:"Created", 400:"BAD REQUEST", 
                   403:"Forbidden", 404:"Not Found", 411:"Length Required", 
                   500:"Internel Server Error", 501:"Not Implemented", 505:"HTTP Version Not Supported"}

    def __init__(self, resp_code, http_version, resp_body, method) -> None:
        """initiates the instance for this class"""
        self.__resp_code = resp_code
        self.__http_version = http_version
        self.__resp_body = resp_body
        self.__method = method

    def generate_response(self) -> str:
        """Generates server responsne based on the response code and body

        Return:
            serv_resp: server response
        """
        serv_resp = self.__http_version 
        serv_resp += " " + str(self.__resp_code)
        serv_resp += " " + str(HttpServerResponse.STATUS_CODE.get(self.__resp_code)) + "\n"

        if self.__resp_code < 299:
            tmp_body_list = self.__resp_body.split("\n")
            if tmp_body_list[0].strip() == "<!DOCTYPE html>":
                serv_resp += "\n"
            elif self.__resp_body.split(" ")[0].strip() == "Welcome":
                serv_resp += "\n"
            elif self.__method == "PUT":
                serv_resp += '\n'
            elif self.__method == "DELETE":
                serv_resp += '\n'
            
            serv_resp += self.__resp_body

            return serv_resp
        else:
            serv_resp += "\n" + str(HttpServerResponse.STATUS_CODE.get(self.__resp_code))
        

        return serv_resp.strip()
        

            

