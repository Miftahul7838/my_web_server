import argparse
import os, sys
# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the absolute path of the project root directory
project_root_dir = os.path.abspath(os.path.join(current_script_dir, '..'))
# Add the project root directory to sys.path
sys.path.append(project_root_dir)
from lib.argvalidation import ArgValidation as Aval
import logging
import socket
import ssl
from threading import Thread
import subprocess

pub_cert_file = None
priv_key_file = None
is_https = False

def parse_arguments() -> argparse.Namespace:
    """The parser for the provided argument on the terminal

    Returns:
        args: the arguments that were used in the terminal
    """
    global is_https, pub_cert_file, priv_key_file
    # creating the parser object
    parser = argparse.ArgumentParser(
        description="A http(s) webserver",
        epilog="""
        Use "./webserver.py IP PORT --cert example.pem --key example.key" to start the webserver with TLS -OR-
        Use "./webserver.py IP PORT" to start the webser without TLS
        """
    )
    # adding argument to the parser that can be used with this script
    parser.add_argument('ip_address', metavar="IP", type=str, action=Aval, help="The IP address to start on")
    parser.add_argument('port', metavar="PORT", type=int, action=Aval, help="The port to listen to")
    group = parser.add_argument_group(title="Optional argument", description="if you use these options, then both must be used")
    group.add_argument("--cert", required=False, type=argparse.FileType('r'), help="The certificate file")
    group.add_argument("--key", required=False, type=argparse.FileType('r'), help="Corresponding key file of the certificate")
    args = parser.parse_args()
    # conditions to make sure all the neccesarry files are provided when using certain optoins
    if args.cert and not args.key:
        parser.error("--key [example.key] is required when --cert [example.pem] is provided")
    elif args.key and not args.cert:
        parser.error("--cert [example.pem] is required when --key [example.key] is provided")
    elif args.cert and args.key:
        is_https = True
        pub_cert_file = str(args.cert.name)
        priv_key_file = str(args.key.name)
    return args

def rec_http_req(conn) -> str:
    """Gets the clinet's http request

    Args:
        conn: the connection to the client
    Return:
        http_request: the client's https request
    """
    timeout_time = 1
    conn.settimeout(timeout_time)
    # getting the client http request
    http_request = ""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            http_request += data.decode()
    except socket.timeout:
        print(f"Socket timed out for {timeout_time}. Stopped recieving client request")
    return http_request

def log_http_req(http_req, client_ip, client_port) -> None:
        """Loggs the first line of the http request

        Args:
            http_req: the http request of the client
            client_ip: the ip address of the client
            client_port: the port of the client
        """
        req_start_line = http_req.split("\n")[0]
        log_msg = "From IP:" + str(client_ip) + ",Port:" + str(client_port) + ",msg:" + str(req_start_line)
        # logging the first line of the http request
        logging.info(log_msg)

def get_serv_resp(http_req) -> str:
    """gets the server http response based the client http request.

    Args:
        http_req: the client http request
    """
    print(http_req)
    cmd = f'cd ../src/; echo "{http_req}" > httpReq.txt; python3 ./http_parser.py httpReq.txt'
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out = p.stdout.decode()
    err = p.stderr.decode()
    print(out)
    return out

def handler(sock, logfile, client_ip, client_port) -> None:
    """Handle a new client connection

    Args:
      sock: The client socket.
      logfile: The filename to write logs to
      client_ip: the ip of the client
      client_port: the port the clinet used to connect on their end
    """
    global pub_cert_file, priv_key_file, is_https
    if is_https:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(pub_cert_file, priv_key_file)
    # setting logging configuration
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    # Procening client request and server response
    if is_https: # if the webserver is started with TLS certificate
        with context.wrap_socket(sock, server_side=True) as ssock:
            # getting clinet http request
            http_req = rec_http_req(ssock)
            # the server http response
            resp = get_serv_resp(http_req)
            # logging the first line of the https request
            log_http_req(http_req, client_ip, client_port)
            # sending server response data
            ssock.sendall(resp.encode())

    elif not is_https: # if the webserver is started without TLS certificate
        # getting clinet http request
        http_req = rec_http_req(sock)
        # the server http response
        resp = get_serv_resp(http_req)
        # logging the first line of the https request
        log_http_req(http_req, client_ip, client_port)
        # sending server response data
        sock.sendall(resp.encode())
        sock.close()
            
def main() -> None:
    """Starts the webserver.
    """
    global pub_cert_file, priv_key_file
    # getting the argument in the terminal to this webserver script
    arguments = parse_arguments()
    # setting the IP and the port to use
    ip_address = arguments.ip_address
    port = arguments.port
    # creating the log file
    log_path_filename = '../logs/webserv.log'
    # setting the socket to recive connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        try:
            sock.bind((ip_address, port))
        except PermissionError:
            print("PermissionError: You do not have permission to bind to the specified IP address and port.")
            sys.exit(1)
        sock.listen(5)
        # coninuously accepting connections
        while True:
            connection, addr = sock.accept()
            client_ip, client_port = addr
            t = Thread(target=handler, args=(connection,log_path_filename, client_ip, client_port))
            t.start()

if __name__ == '__main__':
    main()