#!/usr/bin/env python
import cherrypy
import os
import sys
import threading
import traceback
import webbrowser
import json
import datetime

from base64 import b64encode
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError


class OAuth2Server:
    def __init__(self, client_id, client_secret,
                 redirect_uri='http://127.0.0.1:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.success_html = """
            <h1>You are now authorized to access the Fitbit API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""

        self.fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            timeout=10,
        )

    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.fitbit.client.authorize_token_url()
        # Open the web browser in a new thread for command-line browser support
        threading.Timer(1, webbrowser.open, args=(url,)).start()
        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()


def loadConfigFile(filename):
    f = open(filename, 'r')
    jsonData = json.load(f)
    param = {}
    param['client_id'] = jsonData['client_id']
    param['client_secret'] = jsonData['client_secret']
    param['token_file'] = jsonData['token_file']
    return param

def saveTokenData(d, filename):
    key_list = ['access_token', 'refresh_token', 'expires_in', 'expires_at']
    f2 = open(filename,'w')
    f2.write('{' + '\n')
    
    expires_value = -1
    msg = ''
    for key, value in d:
        if key in key_list:
            f2.write('   "{0}": "{1}",'.format(key, value) + '\n')
            if key == 'expires_at':
                expires_value = value
    
    if expires_value > 0:
        expires_dt =  datetime.datetime.fromtimestamp(expires_value)
        s = str(expires_dt)
        f2.write('   "expires": "{0}"'.format(s) + '\n')
        msg = '有効期限 {0} までのトークンを取得しました!'.format(s) + '\n'
        msg = msg + '詳細はJSONファイル {0} をご覧ください!'.format(filename)
    
    f2.write('}' + '\n')
    f2.close()

    if expires_value > 0:
        print(msg)


if __name__ == '__main__':
    config_filename = 'config.json'
    param = loadConfigFile(config_filename)

    server = OAuth2Server(param['client_id'], param['client_secret'])
    server.browser_authorize()

    profile = server.fitbit.user_profile_get()
    print('You are authorized to access data for the user: {}'.format(
        profile['user']['fullName']))

    print('TOKEN\n=====\n')
    saveTokenData(server.fitbit.client.session.token.items(), param['token_file'])
