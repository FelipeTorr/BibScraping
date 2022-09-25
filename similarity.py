#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:33:15 2021

@author: felipe
"""
import numpy as np

def signatureWord(word,maximum=220):
    #Calculate an ad-hoc signature code from a word
    signature=[]
    #append the length of the word
    signature.append(len(word))
    #append the first letter with ponderation x3
    signature.append(np.min([ord(word[0]),maximum-1]))
    signature.append(np.min([ord(word[0]),maximum-1]))
    if len(word)>3:
        for i in range(len(word)-3):
            #append the characters ascci code 
            signature.append(np.min([ord(word[i]),maximum-1]))
            #append the combination of three letters or the maximnum code
            #This reduces the weight of the two final letters, then 
            #this removes some plurals
            signature.append(np.min([(3*ord(word[i])+2*ord(word[i+1])+ord(word[i+2]))%maximum,maximum-1]))
    return signature

def signatureName(name,maximum=220):
    #Calculate an ad-hoc signature code from a name
    signature=[]
    if len(name)>0:
    #append the first letter with ponderation x3
        signature.append(np.min([ord(name[0]),maximum-1]))
        signature.append(np.min([ord(name[0]),maximum-1]))
        for i in range(len(name)-3):
            signature.append(np.min([(2*ord(name[i])+ord(name[i+1]))%maximum,maximum-1]))
            #append triple the first letter after spaces
            if ord(name[i])==32:
                signature.append(np.min([ord(name[i]),maximum-1]))
                signature.append(np.min([ord(name[i]),maximum-1]))
                signature.append(np.min([2*ord(name[i+1]),maximum-1]))
        if not ord(name[-1])==46:
            signature.append(ord(name[-1]))
    else:
        signature.append(0)
    return signature

def occurrence_matrix(textlist,N=220,names=False):
    #textlist: list of words
    #N: len of signature codes
    occurrence_matrix=np.zeros((len(textlist),N))
    #populate the matrix
    for i,text in zip(range(len(textlist)),textlist):
        if names:
            pos=signatureName(text)
        else:
            pos=signatureWord(text)
        for m in pos:
            occurrence_matrix[i,m]+=1
    #Normalize
    normaliz=np.linalg.norm(occurrence_matrix,axis=1)
    for col in range(N):
        suma_col=np.sum(occurrence_matrix[:,col])
        if suma_col>0:
            occurrence_matrix[:,col]=occurrence_matrix[:,col]/normaliz
    return occurrence_matrix

def vector_cos_similarity(text,matrix,N=220,names=False):
    vect=np.zeros((1,N))
    if names:
        pos=signatureName(text)
    else:
        pos=signatureWord(text)
    for m in pos:
            vect[0,m]+=1
    result=np.matmul(vect,matrix.T)
    return result

def cos_similarity(textlist,N=220,names=False):
    matrix=occurrence_matrix(textlist,N=N,names=names)
    matrix=np.matmul(matrix,matrix.T)
    np.fill_diagonal(matrix,0)
    return matrix

def addCode2Dictionary(code,dictionary,similarity_th=0.9,names=False):
    deduplicated_code=code
    if code not in dictionary:
        #new indetification key
        new_idx=len(dictionary)
        #insert the new pair in the dictionary
        dictionary[code]=new_idx
        #Use the values(words) of the dictionary
        key_values=list(dictionary.keys())
        #Calculate the similarity matrix, remove auto-similarity
        similarityMatrix=cos_similarity(key_values,names=names)
        
        #apply the threshold
        similars=np.argwhere(similarityMatrix>similarity_th)
        #If there is already a similar value on the dictionary 
        if len(similars)>0:
            if similars[-1,0]==len(key_values)-1:
                deduplicated_code=key_values[similars[-1,1]]
                #remove last registered value on the dictionary
                del dictionary[code]
    return deduplicated_code, dictionary

def searchCodeDictionary(code,dictionary,N=220,names=False):
    deduplicated_code=code
    key_values=list(dictionary.keys())
    similarityMatrix=occurrence_matrix(key_values,N=N,names=names)
    #apply the threshold
    vector=vector_cos_similarity(code, similarityMatrix)
    similars=np.argmax(vector)
    #If there is already a similar value on the dictionary 
    deduplicated_code=key_values[similars]
    return deduplicated_code


def add_paper_kwords(kword,kwords_array,kword_codes,similarity_th=0.9,names=False):
    #kword: word
    #kwords_array: array(list) of identification key of current article kwords
    #kword_codes: dictionary of indentification keys and words
    if kword in kword_codes:
        kwords_array.append(kword_codes[kword])
    else:
        addCode2Dictionary(kword, kword_codes,similarity_th=similarity_th,names=names)
    return kwords_array, kword_codes

def search_paper_kwords(kword,kwords_array,kword_codes,names=False):
    #kword: word
    #kwords_array: array(list) of identification key of current article kwords
    #kword_codes: dictionary of indentification keys and words
    if kword in kword_codes:
        key=kword
    else:
        key=searchCodeDictionary(kword, kword_codes,names=names)
    kwords_array.append(kword_codes[key])
    return kwords_array
