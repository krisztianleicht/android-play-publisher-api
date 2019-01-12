#!/usr/bin/python
import argparse
import os
import io
import json

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials

def init(argv, name, parents=[], scopes=[]):
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=parents)
  
  with open('service_secrets.json') as f:
    data = json.load(f)

  email = data["email"]
  p12filelocation = data["p12file"]
  
  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with the Credentials. Note that the first parameter, service_account_name,
  # is the Email address created for the Service account. It must be the email
  # address associated with the key that was created.
  credentials = ServiceAccountCredentials.from_p12_keyfile(
      email,
      p12filelocation,
      scopes=scopes)
  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build(name, 'v3', http=http)

  # Process flags and read their values.
  flags = parser.parse_args(argv[1:])
  return (service, flags)