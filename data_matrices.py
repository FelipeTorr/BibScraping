#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:28:09 2021

@author: felipe
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 22:05:28 2021

@author: felipe
"""
import numpy as np
import re
import nltk
import fieldsFormat
import pickle
import similarity
import sys
from pybtex.database.input import bibtex

def sortDictionary(dictionary):
    key_values=list(dictionary.keys())
    key_values.sort()
    new_dict={}
    inverse_dict={}
    
    for n,key in enumerate(key_values):
        new_dict[key]=n
        inverse_dict[n]=key
    return new_dict,inverse_dict

if __name__=="__main__":
    filename=sys.argv[1]
    #Load dictionaries
    dictionaries_file = open('dictionaries.plk', "rb")
    dictionaries=pickle.load(dictionaries_file)
    kwords_dictionary=dictionaries[0] 
    inverse_kwords_dictionary=dictionaries[1]  
    titles_dictionary=dictionaries[2] 
    inverse_titles_dictionary=dictionaries[3] 
    authors_dictionary=dictionaries[4]  
    inverse_authors_dictionary=dictionaries[5]  
    journals_dictionary=dictionaries[6]  
    inverse_journals_dictionary=dictionaries[7] 
    #You can do manual changes if something is not in 'good format' the collected data.
    journals_dictionary.pop('physical review e  statistical, nonlinear, and soft matter physics',None)
    journals_dictionary,inverse_journals_dictionary=sortDictionary(journals_dictionary)
    years_dictionary={}
    inverse_years_dictionary={}
    
    #You can edit here the years (maybe the maximum and the minimum could be collected in the previous sxcript)
    for n,y in enumerate(range(1900,2022)):
        years_dictionary[n]=y
        inverse_years_dictionary[y]=n
    matrix_years_articles=np.zeros((len(years_dictionary.keys()),len(titles_dictionary.keys())))
    matrix_articles_authors=np.zeros((len(titles_dictionary.keys()),len(authors_dictionary.keys())))
    matrix_articles_words=np.zeros((len(titles_dictionary.keys()),len(kwords_dictionary.keys())))
    matrix_articles_journals=np.zeros((len(titles_dictionary.keys()),len(journals_dictionary.keys())))
    matrix_coauthors=np.zeros((len(authors_dictionary.keys()),len(authors_dictionary.keys())))
    #Bibtex
    parser = bibtex.Parser()
    bib_data = parser.parse_file(filename)
    entries_key=bib_data.entries.keys()
    
    n=1
    for entry in entries_key:
        #authors
        print(n)
        n+=1
        key_authors=[]
        key_kwords=[]
        key_titles=[]
        key_journals=[]
        key_years=[]
        for author in bib_data.entries[entry].persons['author']:
            author_name=fieldsFormat.format_name(author)
            key_authors=similarity.search_paper_kwords(author_name, key_authors, authors_dictionary,names=True)
            
        title=fieldsFormat.format_title(bib_data.entries[entry].fields['title'])
        try:
            journal=fieldsFormat.format_title(bib_data.entries[entry].fields['journal'])
        except:
            try:
                journal=fieldsFormat.format_title(bib_data.entries[entry].fields['booktitle'])
            except:
                journal='no journal'
        
        key_journals=similarity.search_paper_kwords(journal,key_journals,journals_dictionary)
        journal_code=key_journals[0]   
        
        year=bib_data.entries[entry].fields['year']
        year_code=inverse_years_dictionary[int(year)]
        title_code=titles_dictionary[title]
        tokens_title=nltk.word_tokenize(title)
        tokens_all=tokens_title
        try:
            abstract=fieldsFormat.format_title(bib_data.entries[entry].fields['abstract'])
            tokens_abstract=nltk.word_tokenize(abstract)
            tokens_all=tokens_title+tokens_abstract
        except:
            print(entry, 'without abstract')
        tagged=nltk.pos_tag(tokens_all)
        key_words_tags=[]
        key_kwords=[]
        for tag in tagged:
            if (tag[1]=='NN' or tag[1]=='NNP' or tag[1]=='NNS' or tag[1]=='JJ' or tag[1]=='VBN') and len(tag[0])>2:
                key_words_tags.append(tag[0].lower())
                
        for word in key_words_tags:
            key_kwords=similarity.search_paper_kwords(word, key_kwords, kwords_dictionary)
        
        matrix_years_articles[year_code,title_code]=1
        matrix_articles_journals[title_code,journal_code]=1
        for author_code in key_authors:
            matrix_articles_authors[title_code,author_code]+=1
            for coauthor_code in key_authors:
                if author_code != coauthor_code:
                    matrix_coauthors[author_code,coauthor_code]+=1
        for word_code in key_kwords:
            matrix_articles_words[title_code,word_code]+=1
    #Save the adjacency matrices
    np.savez('matrices.npz',matrix_years_articles=matrix_years_articles,
    matrix_articles_authors=matrix_articles_authors,
    matrix_articles_words=matrix_articles_words,
    matrix_articles_journals=matrix_articles_journals,
    matrix_coauthors=matrix_coauthors)