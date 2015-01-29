#! /usr/bin/env python

"""Order of execution:
	1. Client (browser) sends request to server.
	2. Server receives the request.
	3. Server passes request to the app.
	4. App sends response to the server.
	5. Server sends app's response to the client.
"""

# Our tutorial's WSGI server.
from wsgiref.simple_server import make_server

def application(environ, start_response):
	"""Creates a WSGI application."""

	# Sorts and stringifies the environment key, value pairs.
	response_body = ['%s: %s' % (key, value) for key, value in sorted(environ.items())]
	response_body = '\n'.join(response_body)

	status = '200 OK'
	response_headers = [('Content-Type', 'text/plain'),
						('Content-Length', str(len(response_body)))]

	start_response(status, response_headers)

	return [response_body]

# Instantiates the WSGI server.
# It will receive the request, pass it to the app,
# and send the app's response to the client.
httpd = make_server(
	'localhost', # The host name.
	8051, # A port number on which to wait for the request.
	application # The app object name, in this case a function.
	)

# Waits for a single request, serves it, and quits.
httpd.handle_request()