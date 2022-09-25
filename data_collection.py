#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 22:05:28 2021

@author: felipe
"""
import numpy as np
import re
import fieldsFormat
import similarity
import nltk
import os
import sys
import pickle
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
    

#%%
if __name__=="__main__":
    filename=sys.argv[1]
    print('Scraping data from', filename)
    #kwords
    kwords_codes={}
    #authors
    authors_codes={}
    #titles
    titles_codes={}
    #journals
    journals_codes={}
    #years
    years_codes={}
    #Bibtex
    parser = bibtex.Parser()
    bib_data = parser.parse_file(filename)
    entries_key=bib_data.entries.keys()
    key_titles=[]
    key_journals=[]
    key_years=[]
    n=1
    for entry in entries_key:
        #authors
        print('Entry',n)
        n+=1
        key_authors=[]
        for author in bib_data.entries[entry].persons['author']:
            author_name=fieldsFormat.format_name(author)
            key_authors,authors_codes=similarity.add_paper_kwords(author_name,key_authors, authors_codes,names=True)
            
        title=fieldsFormat.format_title(bib_data.entries[entry].fields['title'])
        key_titles,titles_codes=similarity.add_paper_kwords(title,key_titles, titles_codes,similarity_th=0.98)
        try:
            journal=fieldsFormat.format_title(bib_data.entries[entry].fields['journal'])
            key_journals,journals_codes=similarity.add_paper_kwords(journal, key_journals, journals_codes)
        except:
            if bib_data.entries[entry]=='article':
                key_journals,journals_codes=similarity.add_paper_kwords('no journal', key_journals, journals_codes)
            elif bib_data.entries[entry]=='book':
                key_journals,journals_codes=similarity.add_paper_kwords('book', key_journals, journals_codes)
            else:
                key_journals,journals_codes=similarity.add_paper_kwords('other', key_journals, journals_codes)
        # year=bib_data.entries[entry].fields['year']
        # key_years,years_codes=add_paper_kwords(year,key_years, years_codes,similarity_th=0.99)
    
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
            key_kwords,kwords_codes=similarity.add_paper_kwords(word, key_kwords, kwords_codes,similarity_th=0.92)
        
        print(title)
    kwords_dictionary,inverse_kwords_dictionary=sortDictionary(kwords_codes)
    
    titles_dictionary,inverse_titles_dictionary=sortDictionary(titles_codes)
    authors_dictionary,inverse_authors_dictionary=sortDictionary(authors_codes)
    journals_dictionary,inverse_journals_dictionary=sortDictionary(journals_codes)
    file_dictionaries=open('dictionaries.plk','wb')
    dictionaries=[kwords_dictionary,inverse_kwords_dictionary,titles_dictionary,inverse_titles_dictionary,
                  authors_dictionary,inverse_authors_dictionary,journals_dictionary,inverse_journals_dictionary]
    pickle.dump(dictionaries,file_dictionaries)
    file_dictionaries.close()