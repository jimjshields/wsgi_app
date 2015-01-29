# Explaining a simple WSGI app.
# Usable implementation w/ real environment dictionary in environ_dict.py.

# This is an app object. It could have any name.
# This won't run on its own as a server hasn't been instantiated yet.
def app(environ, start_response):
	"""environ: a dictionary containing CGI-like environment variables,
	   	which is filled by the server for each received request from the client.
	   start_response: a callback function supplied by the server
	   	which will be used to send the HTTP status and headers to the server."""

	"""Creates a WSGI application with the above arguments."""

	# Builds the response body possibly using the environ dict.
	response_body = 'The request method was %s.' % (environ['REQUEST_METHOD'])

	# HTTP response code and message
	status = '200 OK'

	# These are HTTP headers expected by the client.
	# They must be wrapped as a list of tupled pairs:
	# [(Header name, Header value)].
	# List of header fields: http://en.wikipedia.org/wiki/List_of_HTTP_header_fields
	# List of MIME types: http://en.wikipedia.org/wiki/Internet_media_type
	response_headers = [('Content-Type', 'text/plain'),
						('Content-Length', str(len(response_body)))]

	# Send them to the server using the supplied function.
	# This is why start_response is a callback function - 
	# It is passed as an argument to this function and is then called (back).
	start_response(status, response_headers)

	# Return the response body.
	# Notice it is wrapped in a list, though it could be any iterable.
	return [response_body]