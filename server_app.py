from blessings import Terminal

term = Terminal()

# Taken directly from https://gist.github.com/thomasballinger/5104059
# Annotated for further understanding.

# Socket - used to create socket objects.
# Socket objects can connect to each other using the methods in the socket module.

import socket

def serve(app):
	"""Creates an actual server object on which to serve an app."""
	
	# A socket object represents one endpoint of a network connection.
	# This creates the server socket, which will listen for connections from a client socket.
	# socket([family[, type[, proto]]])

	sock_family = socket.AF_INET
	sock_type = socket.SOCK_STREAM
	sock_proto = 0

	# Creates a new socket object w/ defaults for family, type, proto.
	listener = socket.socket(sock_family, sock_type, sock_proto)

	print createHeader('Creation of Server Socket', colors.GREEN)
	print 'New listener/server socket %s was created with default settings: family %s, type %s, and protocol %s.' % (listener, sock_family, sock_type, sock_proto)
	print 'This socket will listen for connections.'

	# Sets the socket options for the socket object.
	# The below are the default options.
	level = socket.SOL_SOCKET
	optname = socket.SO_REUSEADDR
	value = 1

	listener.setsockopt(level, optname, value)

	print 'Default socket options have been set for %s.' % (listener)
	print 'It has level %s, optname %s, and value %s.' % (level, optname, value)

	# Binds the socket to a local address with host HOST and port PORT.
	HOST = ''
	PORT = 8080

	listener.bind((HOST, PORT))

	print 'Socket has been bound to host "%s" and port %s.' % (HOST, PORT)

	host_pretty = 'localhost' if HOST == '' else HOST

	print createHeader('You can connect to the server at %s:%s' % (host_pretty, PORT), colors.GREEN)

	# Starts listening for incoming connections.
	# socket().listen(num_connections)
	listener.listen(5)
	
	# Continuously listens for connections from any client.
	while True:

		# Any client (e.g., the browser) can connect to the host and port as defined above.
		# They can do this because the socket object (listener) is accepting connections as defined below.
		# When it does accept a connection, it assigns the client socket and address to the below tuple.
		client_socket, client_address = listener.accept()

		print createHeader('Creation of New Client Socket', colors.CYAN)
		print 'New client socket was created.'
		print 'Server received connection from client socket at host %s, port %s.' % (client_address[0], client_address[1])

		# Receives data from the client socket and assigns it.
		# The return value is a string representing the data received.
		# The argument is the buffer size (bufsize) which specifies the max amount of data received at once.
		request = client_socket.recv(10000)

		# Assigns the first part of the request to method. (expects HTTP requests - i.e., GET, POST, etc.)
		# Assigns the remaining part of the request to rest.
		method, rest = request.split(' ', 1)

		# In the remaining part, assigns the path to path, and the remaining part to rest.
		path, rest = rest.split(None, 1)

		print createHeader('Client Request', colors.MAGENTA)

		print createSubHeader('Method')
		print method
		print createSubHeader('Path')
		print path
		print createSubHeader('The rest of the request')
		print rest

		print createHeader('End of Client Request', colors.MAGENTA, new_lines=False)

		# Defines the interface method.
		def start_response(status, headers):
			"""Defines a function for sending a response to a client socket given an HTTP status and HTTP headers."""

			httpResponse = '\r\n'.join(['HTTP/0.9 %s' % (status)] + [k+': '+v for k, v in headers])

			print createHeader('Server HTTP Response', colors.GREY)
			print createSubHeader('Status')
			print status
			print createSubHeader('Headers')
			print headers
			print createSubHeader('Body')
			print httpResponse
			print createHeader('End of Server HTTP Response', colors.GREY)

			# Sends the HTTP response from the server socket to its connected client socket.
			client_socket.send(httpResponse)
			client_socket.send('\r\n\r\n')
		
		# Defines the environment to be used when serving the app.
		environ = {'REQUEST_METHOD': method, 'PATH_INFO': path}
		
		# Sends all data from the listener to the client.
		print createHeader('Server Sending Data to Client', colors.RED)
		for data in app(environ, start_response):
			print data

			client_socket.send(data)

		print createHeader('End Sending Data', colors.RED, new_lines=False)

		client_socket.close()
		print createHeader('Closing Client Socket', colors.CYAN)
		print '%s has been closed.' % (client_socket)
		print createHeader('End of Server/Client Connection', colors.CYAN)

def demo_app(environ, start_response):
	"""Creates an app object that can be served."""

	print createSubHeader('Calling the app')

	# Calls the callback function with HTTP status & headers.
	start_response('200 OK', [('Content-Type', 'text/plain')])

	print createSubHeader('Body')
	# Returns info on the environment; will display to the client.
	return [('You asked to ' + environ['REQUEST_METHOD'] + ' ' + environ['PATH_INFO']), 'second item']

# Utility

class colors(object):
	RED = '\033[91m'
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	WHITE = '\033[97m'
	YELLOW = '\033[93m'
	MAGENTA = '\033[95m'
	GREY = '\033[90m'
	BLACK = '\033[90m'
	DEFAULT = '\033[99m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def createHeader(string, color=colors.DEFAULT, width=None, new_lines=True):
	"""Pads string with dashes for better terminal printing.
	   Allows for color printing."""

	if width == None:
		width = term.width

	length = len(string)
	numDashes = (width - length)/2
	dashes = numDashes * '-'
	if new_lines:
		return wrap_in_newlines(color + dashes + string + dashes + colors.ENDC)
	else:
		return color + dashes + string + dashes + colors.ENDC

def createSubHeader(string, width=None):
	"""Pads string with left-side dashes for better terminal printing.
	   Makes string look like a subheader."""

	if width == None:
		width = term.width

	length = len(string)
	numDashes = (width - length)/2
	dashes = numDashes * '-'
	return colors.BLUE + dashes + string + colors.ENDC

def wrap_in_newlines(string):
	return '\n%s\n' % (string)


if __name__ == '__main__':
	serve(demo_app)