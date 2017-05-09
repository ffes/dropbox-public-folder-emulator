#!/usr/bin/env python3
"""
    Copyright (c) 2017 Frank Fesevur
"""

from wsgiref.simple_server import make_server
import json
import urllib.request
import conf


# The application interface is a callable object
def application(environ, start_response):

    # Build the response body possibly
    # using the supplied environ dictionary
    response_body = 'Request method: %s' % environ['REQUEST_METHOD']

    # HTTP response code and message
    status = '200 OK'

    # HTTP headers expected by the client
    # They must be wrapped as a list of tupled pairs:
    # [(Header name, Header value)].
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]

    # Send them to the server using the supplied function
    start_response(status, response_headers)

    # Return the response body. Notice it is wrapped
    # in a list although it could be any iterable.
    return [response_body.encode()]


def public_folder(environ, start_response):

    # Construct the API request headers
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + conf.oauth_token
    }

    # Get the filename from the request
    path = environ.get("PATH_INFO", "")

    # First see if the file has been shared before
    data = json.dumps( { "path": path } ).encode("utf-8")

    # Do the request
    req = urllib.request.Request("https://api.dropboxapi.com/2/sharing/list_shared_links",
                                data=data, headers=headers)

    try:
        # If we get here the request was successful

        # Get the reponse, decode it and tranform the json in a dictionary
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf8'))

        # get the url from the dictionary
        url = data["links"][0]["url"]

        # Return the HTTP response code and location
        status = "302 Found"
        start_response(status, [("Location", url)])

        return [b'']

    except urllib.error.URLError as e:
        # error code 409 means the file is not shared yet
        if e.code != 409:

            # We have hit an unexpected error
            print(e.reason)
            print(e.read().decode("utf8", 'ignore'))
            start_response("500 Internal server error")
            return [b'']

    # New file. Not shared yet, share it now
    data = json.dumps( { "path": path, "settings": { "requested_visibility": "public" } } ).encode("utf-8")
    req = urllib.request.Request("https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings",
                                data=data, headers=headers)

    try:
        response = urllib.request.urlopen(req)
        data = json.loads(reponse.read().decode('utf8'))

        #print(response.read().decode('utf8'))
        print(data)
        print(data[0]["url"])

        # Return the HTTP response code and location
        status = "302 Found"
        start_response(status, [("Location", url)])

        return [b'']

    except urllib.error.URLError as e:

        if e.code == 409:

            # The requested file is not there
            status = "404 Not Found"
            response_body = 'File Not Found: %s' % path

            # HTTP headers expected by the client
            # They must be wrapped as a list of tupled pairs:
            # [(Header name, Header value)].
            response_headers = [
                ('Content-Type', 'text/plain'),
                ('Content-Length', str(len(response_body)))
            ]

            start_response(status, response_headers)
            return [response_body.encode()]

        print(e.reason)
        print(e.read().decode("utf8", 'ignore'))

        start_response("500 Internal server error")
        return [b'']


#
# https://docs.python.org/3.6/library/wsgiref.html
#

def main():

    if conf.oauth_token == "" or conf.public_folder == "":
        print("Missing configuration!")
        print("Make sure the values in 'conf.py' are set.")
        return

    # Instantiate the server
    httpd = make_server('localhost', 8080, public_folder)

    # Wait for a single request, serve it and quit
    httpd.handle_request()

    # Start the webserver
    #httpd.serve_forever()

if __name__ == "__main__":
    main()
