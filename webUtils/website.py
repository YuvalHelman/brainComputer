import copy
from http.server import HTTPServer, SimpleHTTPRequestHandler
import functools
import re
import sys


class WebHandler(SimpleHTTPRequestHandler):
    functions_dict = {}

    def do_GET(self):
        html_str = ""
        func_to_call = None
        user_id = ""
        try:
            args_tuple = None
            for regex_path_url in WebHandler.functions_dict:
                m = re.match(fr"^{regex_path_url}$", self.path)
                if m:  # Check if something was found
                    args_tuple = m.groups()
                    func_to_call = WebHandler.functions_dict.get(regex_path_url)

            # If no regex corresponding to a function was found to be called with, exit
            if func_to_call is None:
                self.send_response(404)
                self.end_headers()
                return
            ret_code, html_str = func_to_call(*args_tuple)
            self.send_response(ret_code,)
            self.send_header('Content-type', 'text-html')
            self.end_headers()
            self.wfile.write(html_str.encode('utf-8'))
            return
        except Exception as e:
            print("error:", e)
            self.send_response(404)
            self.end_headers()


class Website:
    def __init__(self, *args, **kwargs):
        self.functions_dict = {}  # saves all of the functions that are decorated

    def route(self, url_path):
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                try:
                    ret_val = f(*args, **kwargs)
                    return ret_val
                except Exception as e:
                    return e

            self.functions_dict[url_path] = f
            return wrapper

        return decorator

    def run(self, address):
        web_handler = WebHandler
        WebHandler.functions_dict = copy.deepcopy(self.functions_dict)

        httpd = HTTPServer(address, web_handler)
        httpd.serve_forever()

