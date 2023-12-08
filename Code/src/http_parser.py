import os, sys, json
# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the absolute path of the project root directory
project_root_dir = os.path.abspath(os.path.join(current_script_dir, '..'))
# Add the project root directory to sys.path
sys.path.append(project_root_dir)
with open('../config/server_config.json','r') as file:
    config = json.load(file)
os.environ["WEB_ROOT"] = str(config.get('path'))
os.environ["HTTP_METHODS"] = str(config.get('http_methods'))
import argparse
from lib.argvalidation import ArgValidation as Aval
from lib.http_client_req import HttpClientRequst as hcr
from lib.http_server_resp import HttpServerResponse as hsr
from lib.http_methods_actions.http_get import HttpGet as hg
from lib.http_methods_actions.http_post import HttpPost as hp

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Returns https response according to a http request"
        )
    parser.add_argument("http_req", 
                        metavar="REQUEST", 
                        type=argparse.FileType('r'),
                        action=Aval,
                        help="The file with the http request"
                        )
    args = parser.parse_args()
    return args

def perform_action(http_req) -> str:
    client_req = hcr(http_req)
    result = client_req.is_valid_req()
    ret_code = result[0]
    http_v = ""
    path = ""
    method_resp_body = ""
    method_resp_code = None
    if ret_code == 200:
        if result[1] != None:
            start_line = result[1]
            method = start_line[0]
            path = start_line[1]
            http_v = start_line[2]
            if result[2] != None:
                fields = result[2]
                if result[3] != None:
                    body = result[3]
                    if method == 'POST':
                        cont_len = int(fields.get('content-length'))
                        get_resp = hp(path, cont_len, body).welcome_user()
                        method_resp_code = get_resp[0]
                        method_resp_body = get_resp[1]
                    elif method == "PUT":
                        pass
                if method == 'GET':
                    get_resp = hg(path).get_file_cont()
                    method_resp_code = get_resp[0]
                    method_resp_body = get_resp[1]
                elif method == "HEAD":
                    pass
                elif method == "DELETE":
                    pass

    serv_resp = hsr(method_resp_code, http_v, method_resp_body).generate_response()
    return serv_resp

def main() -> str:
    """The main function of the program
    """
    arguments = parse_arguments()
    http_req = arguments.http_req
    http_resp = perform_action(http_req)
    print(http_resp)

if __name__ == '__main__':
    main()