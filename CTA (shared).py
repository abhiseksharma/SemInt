# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 15:38:54 2022

@author: abhis
"""

""" Querying Wikidata"""

import pandas as pd
import json
import copy
from itertools import chain
from collections import Counter
#from rdflib import Graph

from queryingDbpedia import queryingWikidata

target = pd.read_csv("<path of target file from which to fetch table name and column number>", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget = resultTarget.drop([2], axis=1)

resultTarget["output"] = "" * len(resultTarget)
resultTarget["allReturnedClasses"] = "" * len(resultTarget)

for targetIndex in range(len(resultTarget)):
#    targetIndex = 5
    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('<path of current table>' + target.iloc[targetIndex][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[targetIndex][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn])) # to remove repetition
    
    row = 0
    allClasses = []
    
    for term in iterationList:
#        term = "Ramos Arizpe"
#        term = term.split(',')[-1].strip()
#        term = term.replace(" ", "_")
        
        print(targetIndex, currentColumn, row)
        row += 1
        
        if term in termTypeAllColumnSingleFile:
             continue
#        term = "Sterling Heights"
        try:
            query = "select DISTINCT ?o where  {?s rdfs:label \"" + term + "\"@en . ?s wdt:P31 ?o .}"
        except:
            errorTerms.append(term)
            continue
        
        try:
            queryResult = queryingWikidata(query)
        except:
            errorTerms.append(term)
            continue
        
        typeList = []
        
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['o']['value']
#            if "http://dbpedia.org/ontology/" in iri:
            typeList.append(iri)
            termTypeAllColumnSingleFile[term] = [typeList]
        allClasses = allClasses + typeList

    
    if len(allClasses) != 0: 
    
        freq = Counter(chain(allClasses))
        
        maxFreq = max(freq.values())
        if maxFreq < (len(termTypeAllColumnSingleFile)/2):
            finalClass =  ["http://www.w3.org/2002/07/owl#Thing"]
            resultTarget.at[targetIndex, "output"] = finalClass
        else:
            highestFreqClasses = []
            
            for classURI in freq:
                if freq[classURI] == maxFreq:
                    highestFreqClasses.append(classURI)
            
            resultTarget.at[targetIndex, "output"] = highestFreqClasses
            
    
        resultTarget.at[targetIndex, "allReturnedClasses"] = allClasses
        

resultTest = copy.deepcopy(resultTarget)
resultTest = resultTest.drop(["allReturnedClasses"], axis=1)

for i in range(len(resultTest)):
#    resultTest.at[i, 'output'] = ', '.join(resultTest.iloc[i]['output'])
    if len(resultTest.iloc[i]['output']) != 0:
        resultTest.at[i, 'output'] = resultTest.iloc[i]['output'][0]

resultTarget.to_csv("<path of output file for whole result>")
resultTest.to_csv("<path of output file in desired format required for SemTab submission>")
