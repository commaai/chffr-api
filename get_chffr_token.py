#!/usr/bin/env python
import argparse
import sys
from oauth2client import client
import requests
import json

DEFAULT_CLIENT_ID = "45471411055-m902j8c6jo4v6mndd2jiuqkanjsvcv6j.apps.googleusercontent.com"
DEFAULT_CLIENT_SECRET = "it5cGajZGSHQw5-e2kn2zL_R"
SCOPE = u'https://www.googleapis.com/auth/userinfo.email'

if __name__ == '__main__':
  flow = client.OAuth2WebServerFlow(
      client_id=DEFAULT_CLIENT_ID,
      client_secret=DEFAULT_CLIENT_SECRET,
      scope=SCOPE,
      user_agent='comma.ai API example',
      redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  authorize_url = flow.step1_get_authorize_url()

  print ('Log into the Google Account you use to access your comma.ai chffr account'
         ' and go to the following URL: \n%s\n' % (authorize_url))
  print 'After approving the token enter the verification code (if specified).'
  code = raw_input('Code: ').strip()

  try:
    credential = flow.step2_exchange(code)
  except client.FlowExchangeError, e:
    print 'Authentication has failed: %s' % e
    sys.exit(1)

  print "access token: ", credential.access_token
  r = requests.get("https://api.comma.ai/v1/auth/?access_token="+credential.access_token)
  print "got", r.text

  open("chffr_token","w").write(json.loads(r.text)['access_token'])
  print "wrote chffr_token, you are logged in!"



