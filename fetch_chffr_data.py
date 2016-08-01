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
  print my_routes[k]
  print k, my_routes[k]['len']
  route_url = my_routes[k]['url']
  print "secret route url:", route_url

  # fetch coords for route
  coords = json.loads(requests.get(route_url+"/route.coords").text)
  print coords[0:10]

  # fetch first picture for route
  PICTURE_INDEX = 34
  pic_coords = coords[PICTURE_INDEX-1]
  pic = requests.get(route_url+"/sec%d.jpg" % PICTURE_INDEX).content
  print "got picture", len(pic)
  fn = "/tmp/chffr-%.4f-%.4f.jpg" % (pic_coords['lat'], pic_coords['lng'])
  with open(fn, "w") as f:
    f.write(pic)
  print "wrote to", fn

  # only one route for now
  break

