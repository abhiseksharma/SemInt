# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:30:15 2022

@author: user
"""

import requests
import pandas as pd
import numpy as np


from SPARQLWrapper import SPARQLWrapper, JSON

def GetPossibleMappingMain(entity):
    
    for i in entity:
        
        sparql = SPARQLWrapper(
            "https://query.wikidata.org/sparql"
        )
        sparql.setReturnFormat(JSON)
        sparql.setTimeout(40)
        # gets the first 3 geological ages
        # from a Geological Timescale database,
        # via a SPARQL endpoint
        sparql.setQuery("""
           SELECT  ?partOf WHERE {
              ?word rdfs:label \""""+entity+"""\"@en;

                     wdt:P31 ?partOf.
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            LIMIT 3


            """
        )
        output = []
        try:
            ret = sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                output.append(r['partOf']['value'])
            
        except Exception as e:
            print(e)
            
        result = " ".join(output)
        
    return result

def GetPossibleMapping(entity):
    
    for i in entity:
        sparql = SPARQLWrapper(
            "https://query.wikidata.org/sparql"
        )
        sparql.setReturnFormat(JSON)
        sparql.setTimeout(40)
        # gets the first 3 geological ages
        # from a Geological Timescale database,
        # via a SPARQL endpoint
        sparql.setQuery("""
           SELECT  ?partOf WHERE {
              ?word rdfs:label \""""+entity+"""\"@en;
                    wdt:P921 ?main .
              ?main  wdt:P31 ?partOf.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

            }
            LIMIT 3


            """
        )
        output = []
        try:
            ret = sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                output.append(r['partOf']['value'])
            
        except Exception as e:
            print(e)
            
        result = " ".join(output)
        
    return result




def search_entities(query, language='en'):
    payload = {
    'action': 'wbsearchentities',
    'format': 'json',
    'limit': 1,
    'language': language,
    'search': query,
      }
    
    r = requests.get('https://www.wikidata.org/w/api.php', payload)
    data = r.json()
    
    entities = data.get('search')
    label = entities[0].get('label') if entities else None
    
    return label


df = pd.read_csv("CTA_2T_Targets.csv",names=["filename","column_index"])


resultant_df = df.copy()
resultant_df["Wikki_match"] = np.nan

for i,j in enumerate(df.filename):
    path = "C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/tables/"+j+".csv"
    df1 = pd.read_csv(path)
    column_number = (df.column_index.iloc[i])
    column_name = df1.columns[column_number]
    result = []
    count = 0 
    count2 = 0 
    for k in np.unique(df1[column_name]):
        print(k,end="  -> ")
        entity = search_entities(k)
        print(entity)
        if entity is not None :
            temp = GetPossibleMappingMain(entity)
            if temp == None:
                temp = GetPossibleMappingMain(entity)
            result+= temp.split()
            if count >10:
                break
            count+=1
        if count2 > 30 :
            break
        count2+=1
    unique , count = np.unique(np.array(result) , return_counts=True)
    for m , n in zip(unique,count):
        if n == max(count):
            if resultant_df.Wikki_match.isnull().iloc[i]:
                resultant_df.Wikki_match.loc[i]= m
            else:
                resultant_df.Wikki_match.loc[i]= resultant_df.Wikki_match.iloc[i]+m
            print(m)
    print("-"*20)