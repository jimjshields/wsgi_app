# Taken directly from https://gist.github.com/thomasballinger/5104059
# Annotated for further understanding.

# Socket - used to establish connection b/w client & server.
import socket

def serve(app):
	"""Creates an actual server object on which to serve an app."""
	listener = socket.socket()
	listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listener.bind(('', 8080))
	listener.listen(5)
	
	# Constinuously listens for connections.
	while True:
		s, addr = listener.accept()
		print 'Server received connection from', addr
		request = s.recv(10000)
		print 'Request we received: %s' % (request)
		method, rest = request.split(' ', 1)
		path, rest = rest.split(None, 1)

		def start_response(status, headers):
			print 'Sending headers'
			stuff = '\r\n'.join(['HTTP/0.9%s' % (status)] + [k+': '+v for k, v in headers])
			print stuff
			s.send(stuff)
			s.send('\r\n\r\n')
		
		environ = {'REQUEST_METHOD': method, 'PATH_INFO': path}
		
		for data in app(environ, start_response):
			print 'Sending data'
			s.send(data)
		s.close()

def demo_app(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/plain')])
	return [('You asked to ' + environ['REQUEST_METHOD'] + ' ' + environ['PATH_INFO']), 'asdf']

if __name__ == '__main__':
	serve(demo_app)