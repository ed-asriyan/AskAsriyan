from pprint import pformat
from cgi import parse_qsl


def application(environ, start_response):
    output = []

    output.append('<form method="post">')
    output.append('<input type="text" name = "data">')
    output.append('<input type="submit" value="Send post data">')
    output.append('</form>')

    d = parse_qsl(environ['QUERY_STRING'])
    if environ['REQUEST_METHOD'] == 'POST':
        output.append(pformat(environ['wsgi.input'].read()))

    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            for ch in d:
                output.append('<label>')
                output.append(' = '.join(ch))
                output.append('</label>')

    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'), ('Content-Length', str(output_len))])

    return output
