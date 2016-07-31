#!/usr/bin/env python
import requests
import json

# load the access_token
access_token = open("chffr_token").read()

def endpoint(x):
  r = requests.get("https://api.comma.ai/v1/"+x, headers={'Authorization': "JWT "+access_token})
  return json.loads(r.text)

# fetch user info
print endpoint("me")

# fetch routes
my_routes = endpoint("me/routes")['routes']
for k in my_routes:
  print k, my_routes[k]['len']
  route_url = my_routes[k]['url']
  print "secret route url:", route_url

  # fetch coords for route
  coords = json.loads(requests.get(route_url+"/route.coords").text)
  print coords[0:10]

  # fetch first picture for route
  PICTURE_INDEX = 1
  pic = requests.get(route_url+"/sec%d.jpg" % PICTURE_INDEX).content
  print "got picture", len(pic)
  with open("/tmp/chffr.jpg", "w") as f:
    f.write(pic)
  print "wrote to /tmp/chffr.jpg"

  # only one route for now
  break

