# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 16:18:56 2022

@author: abhisek
"""

import pandas as pd
import json


from queryingDbpedia import queryingDBpedia


target = pd.read_csv("CTA_2T_Targets.csv", header=None)

termTypeAllColumn = dict()

listOfFile = list(set(target.iloc[:,0]))

errorTerms = []

for i in range(len(target)):
#for i in range(len(listOfFile)):
    #    print(target.iloc[i])
    currentFile = pd.read_csv('tables/' + target.iloc[i][0] + '.csv') #for working with complete list of files and columns
#    currentFile = pd.read_csv('tables/' + listOfFile[i] + '.csv') #For testing with only 0th column
    currentColumn = target.iloc[i][1]
    
    
    for j in range(len(currentFile.index)):
        term = currentFile.iloc[j][currentColumn]
        term = term.replace(" ", "_")
        print(i, j, currentColumn)
        
#        try:
#            termTypeAllColumn[term]
#            continue
#        except:
#            pass
        
        if term in termTypeAllColumn:
#        if termType.has_key(term):
#            if len(termType[term]) == 1:
#                termType[term] = [termType[term], target.iloc[i][0]]
            continue
        query = """select distinct ?Concept where {<http://dbpedia.org/resource/""" + term + """> a ?Concept}"""
        
        try:
            queryResult = queryingDBpedia(query)
        except:
            errorTerms.append(term)
            continue
        
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['Concept']['value']
            if "http://dbpedia.org/ontology/" in iri:
                termTypeAllColumn[term] = [iri, target.iloc[i][0], str(currentColumn)]
#                termTypeAll[term] = [iri, listOfFile[i]]
                break
            
            
''' termType is a file with only terms of 0th index  '''            
with open("termTypeAllColumn.json", "w") as f:
    #Write it to file
    #f.write(str(result)) 
    json.dump(termTypeAllColumn, f)
    
    
f = open("termTypeAllColumn.json")
termTypeAllColumn = json.load(f)


#for i in termTypeAllColumn:
##    print(i)
#    termTypeAllColumn[i][2] = str(termTypeAllColumn[i][2])


#Dwayne "the rock" johnson