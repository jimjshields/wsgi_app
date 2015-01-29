#! /usr/bin/env python

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