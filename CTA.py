# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 16:18:56 2022

@author: abhisek
"""

import pandas as pd
import json
import rdflib

from queryingDbpedia import queryingDBpedia

target = pd.read_csv("CTA_2T_Targets.csv", header=None)

termTypeAllColumn = dict()

#listOfFile = list(set(target.iloc[:,0]))

errorTerms = []

for i in range(len(target)):
    currentFile = pd.read_csv('tables/' + target.iloc[i][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[i][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn]))
    
    col = 0
    
    for term in iterationList:
        print(i, col, currentColumn)
        col += 1
        
        if term in termTypeAllColumn:
             continue
        
        try:
            query = """select distinct ?Concept where {<http://dbpedia.org/resource/""" + term + """> a ?Concept}"""
        except:
            errorTerms.append(term)
            continue
        
        try:
            queryResult = queryingDBpedia(query)
        except:
            errorTerms.append(term)
            continue
        
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['Concept']['value']
            if "http://dbpedia.org/ontology/" in iri:
                termTypeAllColumn[term] = [iri, target.iloc[i][0], str(currentColumn)]
                break
    
    
#for i in range(len(target)):
#    currentFile = pd.read_csv('tables/' + target.iloc[i][0] + '.csv') #for working with complete list of files and columns
#    currentColumn = target.iloc[i][1]  
#    
#    for j in range(len(currentFile.index)):
#        term = currentFile.iloc[j][currentColumn]
#        term = term.replace(" ", "_")
#        print(i, j, currentColumn)
#        
# #        try:
# #            termTypeAllColumn[term]
# #            continue
# #        except:
# #            pass
#        
#        if term in termTypeAllColumn:
# #        if termType.has_key(term):
# #            if len(termType[term]) == 1:
# #                termType[term] = [termType[term], target.iloc[i][0]]
#            continue
#        
#        try:
#            query = """select distinct ?Concept where {<http://dbpedia.org/resource/""" + term + """> a ?Concept}"""
#        except:
#            errorTerms.append(term)
#            continue        
##        query = """select distinct ?Concept where {<http://dbpedia.org/resource/""" + term + """> a ?Concept}"""
#        
#        try:
#            queryResult = queryingDBpedia(query)
#        except:
#            errorTerms.append(term)
#            continue
#        
#        for k in range(len(queryResult["results"]["bindings"])):
#            iri = queryResult["results"]["bindings"][k]['Concept']['value']
#            if "http://dbpedia.org/ontology/" in iri:
#                termTypeAllColumn[term] = [iri, target.iloc[i][0], str(currentColumn)]
# #                termTypeAll[term] = [iri, listOfFile[i]]
#                break
            
            
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








''' Running for single file'''


import pandas as pd
import json
import copy
#from rdflib import Graph

from queryingDbpedia import queryingDBpedia

target = pd.read_csv("CTA_2T_Targets.csv", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget["output"] = "" * len(resultTarget)

#allSuperClasses = []

for targetIndex in range(20):
    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('tables/' + target.iloc[11][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[11][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn]))
    
    row = 0
    
    for term in iterationList:
#        term = "Ramos Arizpe"
        term = term.split(',')[-1].strip()
        term = term.replace(" ", "_")
        
        print(targetIndex, row, currentColumn)
        row += 1
        
        if term in termTypeAllColumnSingleFile:
             continue
#        term = "Sterling_Heights"
        try:
            query = """select distinct ?Concept where {<http://dbpedia.org/resource/""" + term + """> a ?Concept}"""
        except:
            errorTerms.append(term)
            continue
        
        try:
            queryResult = queryingDBpedia(query)
        except:
            errorTerms.append(term)
            continue
        
        
        typeList = []
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['Concept']['value']
            if "http://dbpedia.org/ontology/" in iri:
                typeList.append(iri)
            termTypeAllColumnSingleFile[term] = [typeList, target.iloc[targetIndex][0]]
    
    
    ''' Common class'''
    
    common = []
    for i in termTypeAllColumnSingleFile:
        if common == []:
            common = termTypeAllColumnSingleFile[i][0]
            continue
        common = set(common).intersection(termTypeAllColumnSingleFile[i][0])
    
    common = list(common)
    
    #dbpedia_graph = Graph()
    #dbpedia_graph.parse("dbpedia_2016-10.owl")
    
    allSuperClasses = []
    
    for concept in common:
        querySubclass = "select distinct ?class where {<" + concept + "> rdfs:subClassOf+ ?class}"
        queryResult = queryingDBpedia(querySubclass)
        for index in range(len(queryResult["results"]["bindings"])):
            allSuperClasses.append(queryResult["results"]["bindings"][index]['class']['value'])
            
            
#    from itertools import chain
#    from collections import Counter
#    
#    freq = Counter(chain(allSuperClasses))
    
    finalClass =  list(set(common).difference(set(allSuperClasses)))
    
    resultTarget.at[targetIndex, "output"] = finalClass
    
    
#    print(finalClass)

''' Finalizing single class '''
#if len(common) > 1:
#    pass


''' Finding interesection then subtracting all the superclasses '''

import pandas as pd
import json
import copy
#from rdflib import Graph

from queryingDbpedia import queryingDBpedia

target = pd.read_csv("CTA_2T_Targets.csv", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget["output"] = "" * len(resultTarget)

#allSuperClasses = []

for targetIndex in range(20):
    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('tables/' + target.iloc[11][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[11][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn]))
    
    row = 0
    
    for term in iterationList:
#        term = "Ramos Arizpe"
        term = term.split(',')[-1].strip()
        term = term.replace(" ", "_")
        
        print(targetIndex, row, currentColumn)
        row += 1
        
        if term in termTypeAllColumnSingleFile:
             continue
#        term = "Sterling_Heights"
        try:
            query = """select distinct ?Concept where {<http://dbpedia.org/resource/""" + term + """> a ?Concept}"""
        except:
            errorTerms.append(term)
            continue
        
        try:
            queryResult = queryingDBpedia(query)
        except:
            errorTerms.append(term)
            continue
        
        
        typeList = []
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['Concept']['value']
            if "http://dbpedia.org/ontology/" in iri:
                typeList.append(iri)
            termTypeAllColumnSingleFile[term] = [typeList, target.iloc[targetIndex][0]]
    
    
    ''' Common class'''
    
    common = []
    for i in termTypeAllColumnSingleFile:
        if common == []:
            common = termTypeAllColumnSingleFile[i][0]
            continue
        common = set(common).intersection(termTypeAllColumnSingleFile[i][0])
    
    common = list(common)
    
    #dbpedia_graph = Graph()
    #dbpedia_graph.parse("dbpedia_2016-10.owl")
    
    allSuperClasses = []
    
    for concept in common:
        querySubclass = "select distinct ?class where {<" + concept + "> rdfs:subClassOf+ ?class}"
        queryResult = queryingDBpedia(querySubclass)
        for index in range(len(queryResult["results"]["bindings"])):
            allSuperClasses.append(queryResult["results"]["bindings"][index]['class']['value'])
            
            
#    from itertools import chain
#    from collections import Counter
#    
#    freq = Counter(chain(allSuperClasses))
    
    finalClass =  list(set(common).difference(set(allSuperClasses)))
    
    resultTarget.at[targetIndex, "output"] = finalClass
    
    
''' Note: There were some blank in the result as intersections were blank in those cases. '''
    
#    print(finalClass)

''' Finalizing single class '''
#if len(common) > 1:
#    pass




''' Finding frequency including superclasses'''

import pandas as pd
import json
import copy
from itertools import chain
from collections import Counter
#from rdflib import Graph

from queryingDbpedia import queryingDBpedia

target = pd.read_csv("CTA_2T_Targets.csv", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget["output"] = "" * len(resultTarget)

for targetIndex in range(20):
#    targetIndex = 5
    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('tables/' + target.iloc[targetIndex][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[targetIndex][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn]))
    
    row = 0
    allClasses = []
    
    for term in iterationList:
#        term = "Ramos Arizpe"
        term = term.split(',')[-1].strip()
        term = term.replace(" ", "_")
        
        print(targetIndex, row, currentColumn)
        row += 1
        
        if term in termTypeAllColumnSingleFile:
             continue
#        term = "Sterling_Heights"
        try:
            query = """select distinct ?Concept where {<http://dbpedia.org/resource/""" + term + """> a ?Concept}"""
        except:
            errorTerms.append(term)
            continue
        
        try:
            queryResult = queryingDBpedia(query)
        except:
            errorTerms.append(term)
            continue
        
        typeList = []
        
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['Concept']['value']
            if "http://dbpedia.org/ontology/" in iri:
                typeList.append(iri)
            termTypeAllColumnSingleFile[term] = [typeList, target.iloc[targetIndex][0]]
        allClasses = allClasses + typeList

    
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
        
        allSuperClasses = []
        
        for concept in highestFreqClasses:
            querySubclass = "select distinct ?class where {<" + concept + "> rdfs:subClassOf+ ?class}"
            queryResult = queryingDBpedia(querySubclass)
            for index in range(len(queryResult["results"]["bindings"])):
                allSuperClasses.append(queryResult["results"]["bindings"][index]['class']['value'])
                
                
    #    from itertools import chain
    #    from collections import Counter
    #    
    #    freq = Counter(chain(allSuperClasses))
        finalClass = []
        finalClass =  list(set(highestFreqClasses).difference(set(allSuperClasses)))
    
        resultTarget.at[targetIndex, "output"] = finalClass
    
    
    
    
""" Saving results """
    
with open("resutlTarget.json", "w") as f:
    #Write it to file
    #f.write(str(result)) 
    json.dump(resultTarget.to_json(orient="split"), f)

resultTarget = json.load(open("resutlTarget.json","r"))

''' Common class'''
#    
#    common = []
#    for i in termTypeAllColumnSingleFile:
#        if common == []:
#            common = termTypeAllColumnSingleFile[i][0]
#            continue
#        common = set(common).intersection(termTypeAllColumnSingleFile[i][0])
#    
#    common = list(common)
#    
#    #dbpedia_graph = Graph()
#    #dbpedia_graph.parse("dbpedia_2016-10.owl")
#    
##    allSuperClasses = []
#    
#    for concept in common:
#        querySubclass = "select distinct ?class where {<" + concept + "> rdfs:subClassOf+ ?class}"
#        queryResult = queryingDBpedia(querySubclass)
#        for index in range(len(queryResult["results"]["bindings"])):
#            allSuperClasses.append(queryResult["results"]["bindings"][index]['class']['value'])
            
    
 
    
""" Querying Wikidata"""

import pandas as pd
import json
import copy
from itertools import chain
from collections import Counter
#from rdflib import Graph



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



from queryingDbpedia import queryingWikidata

target = pd.read_csv("C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/HardtablesR12022/Test/target/cta_target.csv", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget = resultTarget.drop([2], axis=1)

resultTarget["output"] = "" * len(resultTarget)
resultTarget["allReturnedClasses"] = "" * len(resultTarget)

for targetIndex in range(len(resultTarget)):
#    targetIndex = 5
    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/HardtablesR12022/Test/tables/' + target.iloc[targetIndex][0] + '.csv') #for working with complete list of files and columns
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

resultTarget.to_csv("C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/HardtablesR12022/Results/Test/cta_gt_test_with_allclasses.csv")
resultTest.to_csv("C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/HardtablesR12022/Results/Test/cta_gt_test_forsubmission.csv")

#        allSuperClasses = []
        
#        for concept in highestFreqClasses:
#            querySubclass = "select distinct ?class where {<" + concept + "> rdfs:subClassOf+ ?class}"
#            queryResult = queryingDBpedia(querySubclass)
#            for index in range(len(queryResult["results"]["bindings"])):
#                allSuperClasses.append(queryResult["results"]["bindings"][index]['class']['value'])
                
                
    #    from itertools import chain
    #    from collections import Counter
    #    
    #    freq = Counter(chain(allSuperClasses))
#        finalClass = []
#        finalClass =  list(set(highestFreqClasses).difference(set(allSuperClasses)))
    
#        resultTarget.at[targetIndex, "output"] = finalClass


''' To check by selecting different index item in the result '''




""" Querying Wikidata after searching for entity then passing through sparql (13/07/2022)"""

import pandas as pd
import json
import copy
from itertools import chain
from collections import Counter
import requests
import pandas as pd
import numpy as np
#from addressingTypo import addressingTypo
#from rdflib import Graph



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



from queryingDbpedia import queryingWikidata

target = pd.read_csv("C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/HardtablesR12022/Valid/gt/cta_gt.csv", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget = resultTarget.drop([2], axis=1)

resultTarget["output"] = "" * len(resultTarget)
resultTarget["allReturnedClasses"] = "" * len(resultTarget)

for targetIndex in range(len(resultTarget)):
#    targetIndex = 5
    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/HardtablesR12022/Valid/tables/' + target.iloc[targetIndex][0] + '.csv') #for working with complete list of files and columns
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
        
        ''' if query result is empty '''
        if len(queryResult["results"]["bindings"]) == 0:
            entity = search_entities(term)
            try:
                query = "select DISTINCT ?o where  {?s rdfs:label \"" + entity + "\"@en . ?s wdt:P31 ?o .}"
            except:
                errorTerms.append(entity)
                continue
        
            try:
                queryResult = queryingWikidata(query)
            except:
                errorTerms.append(entity)
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

resultTarget.to_csv("C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/HardtablesR12022/Results/Valid/cta_gt_valid_with_allclasses(when null trying search).csv")
resultTest.to_csv("C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/CTA/Code/HardtablesR12022/Results/Valid/cta_gt_valid_forsubmission(when null trying search).csv")


""" Valid"""


""" Querying Wikidata after searching for entity then passing through sparql and addressing typos as well (13/07/2022)"""

import pandas as pd
import json
import copy
from itertools import chain
from collections import Counter
import requests
import pandas as pd
import numpy as np
from addressingTypo import addressingTypo # addressing typo by searching the web
#from rdflib import Graph



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

from queryingDbpedia import queryingWikidata

target = pd.read_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-WD/DataSets/ToughTablesR2-WD/Valid/gt/cta_gt.csv", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget = resultTarget.drop([2], axis=1)

resultTarget["output"] = "" * len(resultTarget)
resultTarget["allReturnedClasses"] = "" * len(resultTarget)

for targetIndex in range(len(resultTarget)):
#    targetIndex = 5

    if target.iloc[targetIndex][0] in resultTarget[0]:
        continue
    
    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-WD/DataSets/ToughTablesR2-WD/Valid/tables/' + target.iloc[targetIndex][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[targetIndex][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn])) # to remove repetition
    
#    iterationList = ["Chemung Cownty", "St. Lawrence Couny", "Chenango ounty"]
    
    row = 0
    allClasses = []

    for term in iterationList:
#        term = "Ramos Arizpe"
#        term = term.split(',')[-1].strip()
#        term = term.replace(" ", "_")
        
        print(targetIndex, currentColumn, row)
        row += 1
        
#        queryResult = dict()
        
        if term in termTypeAllColumnSingleFile:
             continue
#        term = "Sterling Heights"
        try:
            query = "select DISTINCT ?o where  {?s rdfs:label \"" + term + "\"@en . ?s wdt:P31 ?o .}"
        except:
            errorTerms.append(term)
#            continue
        
        try:
            queryResult = queryingWikidata(query)
        except:
            errorTerms.append(term)
#            continue
        
        ''' if query result is empty '''
        if len(queryResult["results"]["bindings"]) == 0:
            entity = search_entities(term)
            try:
                query = "select DISTINCT ?o where  {?s rdfs:label \"" + entity + "\"@en . ?s wdt:P31 ?o .}"
            except:
                errorTerms.append(entity)
#                continue
        
            try:
                queryResult = queryingWikidata(query)
            except:
                errorTerms.append(entity)
#                continue
        
        ''' if even after search query result is empty (maybe because of typo) '''
        if len(queryResult["results"]["bindings"]) == 0:
            entityWithoutTypo = addressingTypo(term)
            try:
                query = "select DISTINCT ?o where  {?s rdfs:label \"" + entityWithoutTypo + "\"@en . ?s wdt:P31 ?o .}"
            except:
                errorTerms.append(entityWithoutTypo)
#                continue
        
            try:
                queryResult = queryingWikidata(query)
            except:
                errorTerms.append(entityWithoutTypo)
#                continue
            
            ''' if typo removed entity has case issue '''
            if len(queryResult["results"]["bindings"]) == 0:
                entity = search_entities(entityWithoutTypo)
                try:
                    query = "select DISTINCT ?o where  {?s rdfs:label \"" + entity + "\"@en . ?s wdt:P31 ?o .}"
                except:
                    errorTerms.append(entity)
#                    continue
            
                try:
                    queryResult = queryingWikidata(query)
                except:
                    errorTerms.append(entity)
#                    continue
        
        typeList = []
        
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['o']['value']
#            if "http://dbpedia.org/ontology/" in iri:
            if iri != "http://www.wikidata.org/entity/Q29654788": # (to remove unicode character entity from the set of candidates)
                typeList.append(iri)
        termTypeAllColumnSingleFile[term] = [typeList]  # why and how to use it??
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

# resultTarget.drop_duplicates()
resultTest = resultTest.drop_duplicates()

resultTarget.to_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-WD/DataSets/ToughTablesR2-WD/Valid/cta_gt_valid.csv")
resultTest.to_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-WD/DataSets/ToughTablesR2-WD/Valid/cta_gt_valid_forsubmission.csv")







""" For Test """

""" Querying Wikidata after searching for entity then passing through sparql and addressing typos as well (13/07/2022)"""

import pandas as pd
import json
import copy
from itertools import chain
from collections import Counter
import requests
import pandas as pd
import numpy as np
from addressingTypo import addressingTypo # addressing typo by searching the web
#from rdflib import Graph



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

from queryingDbpedia import queryingWikidata

target = pd.read_csv("D:/Files/SemTab/Dataset/Round 2/HardTablesR2/DataSets/HardTablesR2/Test/target/cta_target.csv", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

# resultTarget = resultTarget.drop([2], axis=1)

resultTarget["output"] = "" * len(resultTarget)
resultTarget["allReturnedClasses"] = "" * len(resultTarget)

for targetIndex in range(len(resultTarget)):
#    targetIndex = 5

        
    if target.iloc[targetIndex][0] in resultTarget[0]:
        continue

    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('D:/Files/SemTab/Dataset/Round 2/HardTablesR2/DataSets/HardTablesR2/Test/tables/' + target.iloc[targetIndex][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[targetIndex][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn])) # to remove repetition
    
#    iterationList = ["Chemung Cownty", "St. Lawrence Couny", "Chenango ounty"]
    
    row = 0
    allClasses = []

    
    for term in iterationList:
#        term = "Ramos Arizpe"
#        term = term.split(',')[-1].strip()
#        term = term.replace(" ", "_")
        
        print(targetIndex, currentColumn, row)
        row += 1
        
#        queryResult = dict()
        
        if term in termTypeAllColumnSingleFile:
             continue
#        term = "Sterling Heights"
        try:
            query = "select DISTINCT ?o where  {?s rdfs:label \"" + term + "\"@en . ?s wdt:P31 ?o .}"
        except:
            errorTerms.append(term)
#            continue
        
        try:
            queryResult = queryingWikidata(query)
        except:
            errorTerms.append(term)
#            continue
        
        ''' if query result is empty '''
        if len(queryResult["results"]["bindings"]) == 0:
            entity = search_entities(term)
            try:
                query = "select DISTINCT ?o where  {?s rdfs:label \"" + entity + "\"@en . ?s wdt:P31 ?o .}"
            except:
                errorTerms.append(entity)
#                continue
        
            try:
                queryResult = queryingWikidata(query)
            except:
                errorTerms.append(entity)
#                continue
        
        ''' if even after search query result is empty (maybe because of typo) '''
        if len(queryResult["results"]["bindings"]) == 0:
            entityWithoutTypo = addressingTypo(term)
            try:
                query = "select DISTINCT ?o where  {?s rdfs:label \"" + entityWithoutTypo + "\"@en . ?s wdt:P31 ?o .}"
            except:
                errorTerms.append(entityWithoutTypo)
#                continue
        
            try:
                queryResult = queryingWikidata(query)
            except:
                errorTerms.append(entityWithoutTypo)
#                continue
            
            ''' if typo removed entity has case issue '''
            if len(queryResult["results"]["bindings"]) == 0:
                entity = search_entities(entityWithoutTypo)
                try:
                    query = "select DISTINCT ?o where  {?s rdfs:label \"" + entity + "\"@en . ?s wdt:P31 ?o .}"
                except:
                    errorTerms.append(entity)
#                    continue
            
                try:
                    queryResult = queryingWikidata(query)
                except:
                    errorTerms.append(entity)
#                    continue
        
        typeList = []
        
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['o']['value']
#            if "http://dbpedia.org/ontology/" in iri:
            if iri != "http://www.wikidata.org/entity/Q29654788": # (to remove unicode character entity from the set of candidates)
                typeList.append(iri)
        termTypeAllColumnSingleFile[term] = [typeList]  # why and how to use it??
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

resultTarget.to_csv("D:/Files/SemTab/Dataset/Round 2/HardTablesR2/DataSets/HardTablesR2/Test/cta_gt_test_with_allclasses.csv")
resultTest.to_csv("D:/Files/SemTab/Dataset/Round 2/HardTablesR2/DataSets/HardTablesR2/Test/cta_gt_test_forsubmission.csv")





