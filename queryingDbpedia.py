# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 12:21:38 2022

@author: Abhisek
"""

from SPARQLWrapper import SPARQLWrapper, JSON

def queryingDBpedia(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    return sparql.query().convert()


"""Testing"""
#query = """select distinct ?Concept where {<http://dbpedia.org/resource/Honda> a ?Concept}"""
#            
#queryResult = queryingDBpedia(query)
#
#for i in range(len(queryResult["results"]["bindings"])):
#    iri = queryResult["results"]["bindings"][i]['Concept']['value']
#    if "http://dbpedia.org/ontology/" in iri:
#        print(iri)


def queryingWikidata(query):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    return sparql.queryAndConvert()

#query = """select DISTINCT ?o where  {?s rdfs:label "Volvo"@en .
#                ?s wdt:P31 ?o .}"""
#queryResult = queryingWikidata(query)


#sparql?query={SPARQL}&format=json