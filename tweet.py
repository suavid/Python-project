#!/usr/bin/env python
 
import tweepy
import webbrowser 
CONSUMER_KEY = 'WVKInD9ildLix589H5HZA'
CONSUMER_SECRET = 'jpHDkypUv5IAxtsU1HO1gufFNJ7dNf6H5kyRtPiktoo'
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_url = auth.get_authorization_url()
webbrowser.open(auth_url)
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
 
ACCESS_KEY = auth.access_token.key
ACCESS_SECRET = auth.access_token.secret
f = open('keys.py','w')
f.write('#!/usr/bin/env python\n\n')
f.write("CONSUMER_KEY = '"+CONSUMER_KEY+"'\n")
f.write("CONSUMER_SECRET = '"+CONSUMER_SECRET+"'\n")
f.write("ACCESS_KEY = '"+ACCESS_KEY+"'\n")
f.write("ACCESS_SECRET = '"+ACCESS_SECRET+"'\n")
 
f.close()