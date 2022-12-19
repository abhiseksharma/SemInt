# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 00:36:39 2022

@author: user
"""



""" Valid """

import pandas as pd
import json
import copy
from itertools import chain
from collections import Counter
from addressingTypo import addressingTypo
#from rdflib import Graph

from queryingDbpedia import queryingDBpedia

target = pd.read_csv("C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/2022/Round 3/GitTables_SemTab_2022_dbpedia_dataset/semtab_gittables/2022/dbpedia_property_train.csv")

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget["output"] = "" * len(resultTarget)

for targetIndex in range(len(resultTarget)):
#    targetIndex = 5


    if target.iloc[targetIndex][0] in resultTarget.iloc[0]:
        continue

    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/2022/Round 3/GitTables_SemTab_2022_tables/' + target.iloc[targetIndex][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[targetIndex][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn]))
    
    row = 0
    allClasses = []
    
    for term in iterationList:
#        term = "Ramos Arizpe"
        if type(term) != str:
            continue
        term = term.split(',')[-1].strip()
        term = term.replace(" ", "_")
        
        print(targetIndex, currentColumn, row)
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
            # entityWithoutTypo = addressingTypo(term)
            # continue
        
        typeList = []
        
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['Concept']['value']
            if "http://dbpedia.org/ontology/" in iri:
                typeList.append(iri)
            termTypeAllColumnSingleFile[term] = [typeList, target.iloc[targetIndex][0]]
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
    
# resultTest = copy.deepcopy(resultTarget)
# resultTest = resultTest.drop(["allReturnedClasses"], axis=1)

# for i in range(len(resultTest)):
# #    resultTest.at[i, 'output'] = ', '.join(resultTest.iloc[i]['output'])
#     if len(resultTest.iloc[i]['output']) != 0:
#         resultTest.at[i, 'output'] = resultTest.iloc[i]['output'][0]

  
    
# resultTarget.to_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-DBP/DataSets/ToughTablesR2-DBP/Test/cta_gt_test_with_allclasses.csv")
# resultTest.to_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-DBP/DataSets/ToughTablesR2-DBP/Test/cta_gt_test_forsubmission.csv")
resultTarget.to_csv("C:/Users/user/OneDrive/PhD (document or files other than dropbox)/SemTab/2022/Round 3/cta_gt_train_forsubmission.csv")


""" Test """

import pandas as pd
import json
import copy
from itertools import chain
from collections import Counter
from addressingTypo import addressingTypo
#from rdflib import Graph

from queryingDbpedia import queryingDBpedia

target = pd.read_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-DBP/DataSets/ToughTablesR2-DBP/Test/target/cta_target.csv", header=None)

errorTerms = []

resultTarget = copy.deepcopy(target)

resultTarget["output"] = "" * len(resultTarget)

for targetIndex in range(len(resultTarget)):
#    targetIndex = 5


    if target.iloc[targetIndex][0] in resultTarget[0]:
        continue
    
    termTypeAllColumnSingleFile = dict()
    currentFile = pd.read_csv('D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-DBP/DataSets/ToughTablesR2-DBP/Test/tables/' + target.iloc[targetIndex][0] + '.csv') #for working with complete list of files and columns
    currentColumn = target.iloc[targetIndex][1]
    
    iterationList = list(set(currentFile.iloc[:, currentColumn]))
    
    row = 0
    allClasses = []
    
    for term in iterationList:
#        term = "Ramos Arizpe"
        if type(term) != str:
            continue
        term = term.split(',')[-1].strip()
        term = term.replace(" ", "_")
        
        print(targetIndex, currentColumn, row)
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
            # entityWithoutTypo = addressingTypo(term)
            # continue
        
        typeList = []
        
        for k in range(len(queryResult["results"]["bindings"])):
            iri = queryResult["results"]["bindings"][k]['Concept']['value']
            if "http://dbpedia.org/ontology/" in iri:
                typeList.append(iri)
            termTypeAllColumnSingleFile[term] = [typeList, target.iloc[targetIndex][0]]
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
    
# resultTest = copy.deepcopy(resultTarget)
# resultTest = resultTest.drop(["allReturnedClasses"], axis=1)

# for i in range(len(resultTest)):
# #    resultTest.at[i, 'output'] = ', '.join(resultTest.iloc[i]['output'])
#     if len(resultTest.iloc[i]['output']) != 0:
#         resultTest.at[i, 'output'] = resultTest.iloc[i]['output'][0]

  
    
# resultTarget.to_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-DBP/DataSets/ToughTablesR2-DBP/Test/cta_gt_test_with_allclasses.csv")
# resultTest.to_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-DBP/DataSets/ToughTablesR2-DBP/Test/cta_gt_test_forsubmission.csv")
resultTarget.to_csv("D:/Files/SemTab/Dataset/Round 2/ToughTablesR2-DBP/DataSets/ToughTablesR2-DBP/Test/cta_gt_test_forsubmission.csv")