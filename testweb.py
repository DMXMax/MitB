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
import pifacedigitalio
import pygame


JSON_FORMAT = "{{'input_port': {input}, 'output_port': {output}}}"
DEFAULT_PORT = 8000
OUTPUT_PORT_GET_STRING = "output_port"
GET_IP_CMD = "hostname -I"


class PiFaceWebHandler(http.server.BaseHTTPRequestHandler):
    """Handles PiFace web control requests"""
    def do_GET(self):


        # reply with JSON
        self.send_response(200)
        self.send_header("Content-type", "text-html")
        self.end_headers()
#        self.wfile.write(bytes(JSON_FORMAT.format(
 #           input=input_value,
 #          output=output_value,
 #       ), 'UTF-8'))
 
        self.wfile.write(bytes(open("./file.htm", "r").read(),'UTF-8'))

    def set_output_port(self, new_value, old_value=0):
        """Sets the output port value to new_value, defaults to old_value."""
        print("Setting output port to {}.".format(new_value))
        port_value = old_value
        try:
            port_value = int(new_value)  # dec
        except ValueError:
            port_value = int(new_value, 16)  # hex
        finally:
            self.pifacedigital.output_port.value = port_value
            return port_value


def get_my_ip():
    """Returns this computers IP address as a string."""
    ip = subprocess.check_output(GET_IP_CMD, shell=True).decode('utf-8')[:-1]
    return ip.strip()


if __name__ == "__main__":
    # get the port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = DEFAULT_PORT

    # set up PiFace Digital
    PiFaceWebHandler.pifacedigital = pifacedigitalio.PiFaceDigital()
    
    #

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
