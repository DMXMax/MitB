"""
simplewebcontrol.py
Controls PiFace Digital through a web browser. Returns the status of the
input port and the output port in a JSON string. Set the output with GET
variables.

Copyright (C) 2013 Thomas Preston <thomas.preston@openlx.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
ERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import subprocess
import http.server
import urllib.parse
import MitbProp as prop
import concurrent.futures



JSON_FORMAT = "{{'input_port': {input}, 'output_port': {output}}}"
ROUTINES = {'1':prop.trigger1, '2':prop.trigger2, '3':prop.trigger3}
DEFAULT_PORT = 8000
OUTPUT_PORT_GET_STRING = "output_port"
GET_IP_CMD = "hostname -I"

def updateFile( text, replacements):
    for key in replacements.keys():
        text = text.replace(key, replacements[key])
        
    return text


class PiFaceWebHandler(http.server.BaseHTTPRequestHandler):

        
        
    """Handles PiFace web control requests"""
    def do_GET(self):
        worker_status = "Not Busy"
        global prop_worker
        #parse the request.       
        req = urllib.parse.urlparse(self.path)
            
        #print("Test {0}".format(self.test))
        #self.test = self.test+1
        if req.path.endswith('box'):
  
            #if we have an assigned routine, get busy
            if req.query!='':
                qs = urllib.parse.parse_qs(req.query)
                if 'routine' in qs:
                    if prop_worker is not None and not prop_worker.done():
                        worker_status = "Busy - Please Wait"
                    else:
                #
                        prop_worker = self.executor.submit(ROUTINES[qs['routine'][0]])
                        worker_status = "Started"

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            text = open("./box.htm", "r").read()

            text = updateFile(text, {"$Message":worker_status});

            self.wfile.write(bytes(text,'UTF-8'))
        else:
            self.basic_response(req)
        
    
    def basic_response(self, req):
        self.send_response(200)
        self.send_header("Content-type", "text-html")
        self.end_headers()

        text = open("./file2.htm", "r").read()
 
        self.wfile.write(bytes(text,'UTF-8'))
        
        
        


def get_my_ip():
    """Returns this computers IP address as a string."""
    ip = subprocess.check_output(GET_IP_CMD, shell=True).decode('utf-8')[:-1]
    return ip.strip()





"""Main Routine Below"""



if __name__ == "__main__":
    # get the port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = DEFAULT_PORT
        
    # enable the worker thread. This is only to keep the web server getting blocked.
    
    PiFaceWebHandler.executor = concurrent.futures.thread.ThreadPoolExecutor(max_workers =1)
    #set the work thread to none. It will get assigned when we start work.
    prop_worker = None

    print("Monster in the Box started at:\n\n"
          "\thttp://{addr}:{port}\n\n"
          .format(addr=get_my_ip(), port=port))

    # run the server
    server_address = ('', port)
    try:
        httpd = http.server.HTTPServer(server_address, PiFaceWebHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        httpd.socket.close()
