#!/usr/bin/env python

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

html = """
<html>
<body>
   <form method="get" action="parsing_get.wsgi">
      <p>
         Age: <input type="text" name="age">
         </p>
      <p>
         Hobbies:
         <input name="hobbies" type="checkbox" value="software"> Software
         <input name="hobbies" type="checkbox" value="tunning"> Auto Tuning
         </p>
      <p>
         <input type="submit" value="Submit">
         </p>
      </form>
   <p>
      Age: %s<br>
      Hobbies: %s
      </p>
   </body>
</html>"""

def application(environ, start_response):
	"""Creates a callable WSGI application object."""

	# Returns a dict containing lists as values.
	d = parse_qs(environ['QUERY_STRING'])

	# In this idiom you must issue a list containing a default value.
	age = d.get('age', [''])[0] # Returns the first age value.
	hobbies = d.get('hobbies', []) # Returns a list of hobbies.

	# Always escape user input to avoid script injection.
	age = escape(age)
	hobbies = [escape(hobby) for hobby in hobbies]

	response_body = html % (age or 'Empty', ', '.join(hobbies or ['No hobbies']))

	status = '200 OK'

	# Now content type is text/html.
	response_headers = [('Content-Type', 'text/html'),
						('Content-Length', str(len(response_body)))]

	start_response(status, response_headers)

	return response_body

httpd = make_server('localhost', 8051, application)

# Now it is server_forever() instead of handle_request().
# You can kill it in the terminal w/ Ctrl+C.
httpd.serve_forever()