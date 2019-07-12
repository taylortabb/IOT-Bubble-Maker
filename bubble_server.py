#external modules
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import RPi.GPIO as GPIO
import cgi
import time
import requests

# bubble maker ID, this is reported to the google sheet tracking all the worlds bubbles! No other information is reported except for duration of blowing.
# this sheet can be viewed here: https://docs.google.com/spreadsheets/d/17zrNkPzU5HRNvwteC6SXkEnenOMc_gWO7-Ub5Tfj_M0/
# if you do not want your bubble maker reported, just remove the second to last line of this script, starting with requests.post
name="my name"

#GPIO settings
relayPin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relayPin, GPIO.OUT)

#initial relay state: off
GPIO.output(relayPin, GPIO.LOW)

class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        duration = form.getvalue("duration")
        blow(duration)
        
def run(server_class=HTTPServer, handler_class=GP, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ("Server running at localhost", port)
    httpd.serve_forever()

def blow(duration):
    duration=float(duration)
    print('blowing for ',duration,' seconds')
    GPIO.output(relayPin, GPIO.HIGH)
    print('blowing starting')
    time.sleep(duration)
    GPIO.output(relayPin, GPIO.LOW)
    print ('blowing finished')
    #send confirmation of blow to google sheet, tracking all bubble maker blows!
    requests.post(url = "https://script.google.com/macros/s/AKfycbzANUn9p1-takFtazqaqorEhhnixmfF0je0k-iOVWDjgPbE83k/exec", data = {'duration':duration, 'name':name}) 

run()



