# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:04:42 2022

@author: user
"""

#from serpapi import GoogleSearch
#
#params = {
#  "q": "Coffee",
#  "location": "Austin, Texas, United States",
#  "hl": "en",
#  "gl": "us",
#  "google_domain": "google.com",
#  "api_key": "secret_api_key"
#}
#
#search = GoogleSearch(params)
#results = search.get_dict()


#language='en'
#payload = {
#'action': 'wbsearchentities',
#'format': 'json',
#'limit': 1,
#'language': language,
#'search': query,
#  }
#r = requests.get('https://html.duckduckgo.com/html/?q=Tungurahua%20voncano', payload)
#data = r.json()
#r



## We have to import HTML Session
#from requests_html import HTMLSession
## create the Object of the HTMLSession
#session = HTMLSession()
#
##call the get Method of the HTMLSession class
#request = session.get('https://html.duckduckgo.com/html/?q=Tungurahua%20voncano')
#
#data = request.request
#print(data)
#


from requests_html import HTMLSession
session = HTMLSession()
request = session.get('https://html.duckduckgo.com/html/?q=Tungurahua%20voncano')
#data = request.html.links
#print(type(data))
data = request.text
#print(data)
def addressingTypo(term):
    session = HTMLSession()
    request = session.get('https://html.duckduckgo.com/html/?q='+ term)
    data = request.text
    line = data.find("Including results for")
    if line == len(data):
        return None
    queryTermStart = data.find("q=", line)
    
    queryTermEnd = data.find("\">", queryTermStart)
    queryTerm = data[queryTermStart+2:queryTermEnd]
    queryTerm = queryTerm.replace("%20", " ")
    return queryTerm
