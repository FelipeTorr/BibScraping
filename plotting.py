#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 09:23:37 2021

@author: felipe
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import matplotlib.colors as colors
import pickle

def sortDictionary(dictionary):
    key_values=list(dictionary.keys())
    key_values.sort()
    new_dict={}
    inverse_dict={}
    
    for n,key in enumerate(key_values):
        new_dict[key]=n
        inverse_dict[n]=key
    return new_dict,inverse_dict

#Matrices
matrices_file=np.load('matrices.npz')
matrix_years_articles=matrices_file['matrix_years_articles']
matrix_articles_authors=matrices_file['matrix_articles_authors']
matrix_articles_words=matrices_file['matrix_articles_words']
matrix_articles_journals=matrices_file['matrix_articles_journals']
matrix_coauthors=matrices_file['matrix_coauthors']

matrix_years_authors=np.matmul(matrix_years_articles, matrix_articles_authors)
matrix_years_journals=np.matmul(matrix_years_articles, matrix_articles_journals)
matrix_years_words=np.matmul(matrix_years_articles, matrix_articles_words)
matrix_journal_authors=np.matmul(matrix_articles_journals.T,matrix_articles_authors)
matrix_journal_journal1=np.matmul(np.matmul(matrix_journal_authors,matrix_coauthors),matrix_journal_authors.T)/np.max(matrix_coauthors)
matrix_journal_journal=np.matmul(matrix_journal_authors,matrix_journal_authors.T)
matrix_words_authors=np.matmul(matrix_articles_words.T,matrix_articles_authors)
matrix_words_journals=np.matmul(matrix_articles_words.T,matrix_articles_journals)
matrix_words_words=np.matmul(matrix_articles_words.T,matrix_articles_words)/np.max(matrix_articles_words)

#Dictionaries
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
journals_dictionary.pop('physical review e  statistical, nonlinear, and soft matter physics',None)
journals_dictionary,inverse_journals_dictionary=sortDictionary(journals_dictionary)
years_dictionary={}
inverse_years_dictionary={}
for n,y in enumerate(range(1900,2022)):
    inverse_years_dictionary[n]=y
    years_dictionary[y]=n

#Authors
documents_by_author=np.sum(matrix_articles_authors,axis=0)
sort_authors_by_ndocuments=np.flip(np.argsort(documents_by_author))
top_20_authors=sort_authors_by_ndocuments[0:20]
top_20_authors_name=[]
for n in top_20_authors:
    top_20_authors_name.append(inverse_authors_dictionary[n])

#Words
words_by_document=np.sum(matrix_articles_words,axis=0)
sort_words_by_occurrence=np.flip(np.argsort(words_by_document))
top_20_words=sort_words_by_occurrence[0:20]
top_10_words=sort_words_by_occurrence[0:10]
top_20_words_words=[]
top_10_words_words=[]
for i,n in enumerate(top_20_words):
    top_20_words_words.append(inverse_kwords_dictionary[n])
    if i<10:
        top_10_words_words.append(inverse_kwords_dictionary[n])
#Journals
journals_by_year=np.sum(matrix_years_journals,axis=0)
sort_journal_by_occurrence=np.flip(np.argsort(journals_by_year))
top_20_journals=sort_journal_by_occurrence[0:20]
top_20_journals_name=[]
top_10_journals=sort_journal_by_occurrence[0:10]
top_10_journals_name=[]
for i,n in enumerate(top_20_journals):
    top_20_journals_name.append(inverse_journals_dictionary[n])
    if i<10:
        top_10_journals_name.append(inverse_journals_dictionary[n])

#Figuras
fig1=plt.figure(figsize=(14,8.5))
gs1=gridspec.GridSpec(2, 2,hspace=0.5,wspace=0.25)
axA=fig1.add_subplot(gs1[0,0])
axB=fig1.add_subplot(gs1[0,1])
axC=fig1.add_subplot(gs1[1,0])
axD=fig1.add_subplot(gs1[1,1])

axA.bar(list(years_dictionary.keys()),np.sum(matrix_years_articles,axis=1))
axA.set_ylabel('# Documentos')
axA.set_xlabel('Año')

axB.bar(top_20_words_words,words_by_document[top_20_words])
axB.set_xticklabels(top_20_words_words,fontsize=10,rotation=90)
axB.set_ylabel('# Occurrencias')
axB.set_xlabel('Top 20 palabras clave')

    
axC.bar(top_20_authors_name,documents_by_author[top_20_authors])
axC.set_xticklabels(top_20_authors_name,fontsize=10,rotation=90)
axC.set_ylabel('# Documentos')
axC.set_xlabel('Top 20 autores')

top_20_journals_name[4]='sleep medicine'
axD.bar(top_20_journals_name,journals_by_year[top_20_journals])
axD.set_xticklabels(top_20_journals_name,fontsize=10,rotation=90)
axD.set_ylabel('# Documentos')
axD.set_xlabel('Top 20 revistas')

fig1.savefig('Resumen_bibliografia.pdf',dpi=300,bbox_inches='tight')
#%%
fig2=plt.figure(figsize=(7.5,4.7))
axA2=fig2.add_subplot(1,2,1)
im2=axA2.imshow(matrix_years_authors[95::,top_20_authors].T,aspect='auto',interpolation='none',cmap=cm.gist_heat_r,extent=(-0.5,26.5,-0.5,19.5))
axA2.set_yticks(np.arange(0,20))
axA2.set_yticklabels(np.flip(top_20_authors_name))
axA2.set_xticks(np.arange(0,27,2))
axA2.set_xticklabels(np.arange(1995,2022,2),rotation=80)
fig2.colorbar(im2,ax=axA2,shrink=0.4)

axB2=fig2.add_subplot(1,2,2)
normD=colors.Normalize(vmin=0,vmax=np.max(matrix_coauthors))
sorted_matrix_coauthors=matrix_coauthors[top_20_authors,:]
sorted_matrix_coauthors=sorted_matrix_coauthors[:,top_20_authors]
imB2=axB2.imshow(sorted_matrix_coauthors,aspect='equal',interpolation='none',cmap=cm.gist_heat_r,norm=normD,extent=(-0.5,19.5,-0.5,19.5))
axB2.set_ylabel('Co-autores')
axB2.set_xlabel('Autores')
axB2.set_xticklabels('')
axB2.set_yticklabels('')
fig2.colorbar(imB2,ax=axB2,shrink=0.4)


fig3=plt.figure(figsize=(7.5,4.7))
axA3=fig3.add_subplot(1,2,1)
im3=axA3.imshow(matrix_years_journals[95::,top_10_journals].T,aspect='auto',interpolation='none',cmap=cm.gist_heat_r,extent=(-0.5,26.5,-0.5,9.5))
axA3.set_yticks(np.arange(0,10))
axA3.set_yticklabels(np.flip(top_10_journals_name))
axA3.set_xticks(np.arange(0,27,2))
axA3.set_xticklabels(np.arange(1995,2022,2),rotation=90)
clb1=fig3.colorbar(im3,ax=axA3,shrink=0.4)

axB3=fig3.add_subplot(1,2,2)
sorted_matrix_journal_journal=matrix_journal_journal[:,top_10_journals]
sorted_matrix_journal_journal=sorted_matrix_journal_journal[top_10_journals,:]
sorted_matrix_journal_journal=matrix_journal_journal[:,top_10_journals]
sorted_matrix_journal_journal=sorted_matrix_journal_journal[top_10_journals,:]
im4=axB3.imshow(sorted_matrix_journal_journal,interpolation='none',cmap=cm.gist_heat_r,extent=(-0.5,9.5,-0.5,9.5))
axB3.set_ylabel('Journal')
axB3.set_xlabel('Journal')
axB3.set_xticklabels('')
axB3.set_yticklabels('')
clb2=fig3.colorbar(im4,ax=axB3,shrink=0.4)

fig4=plt.figure(figsize=(7.5,4.7))
axA4=fig4.add_subplot(1,2,1)
imA4=axA4.imshow(matrix_years_words[95::,top_10_words].T,aspect='auto',interpolation='none',cmap=cm.gist_heat_r,extent=(-0.5,26.5,-0.5,9.5))
axA4.set_yticks(np.arange(0,10))
axA4.set_yticklabels(np.flip(top_10_words_words))
axA4.set_xticks(np.arange(0,27,2))
axA4.set_xticklabels(np.arange(1995,2022,2),rotation=90)
clb4=fig4.colorbar(imA4,ax=axA4,shrink=0.4)


axB4=fig4.add_subplot(1,2,2)
sorted_matrix_word_word=matrix_words_words[:,top_10_words]
sorted_matrix_word_word=sorted_matrix_word_word[top_10_words,:]
imB4=axB4.imshow(sorted_matrix_word_word,interpolation='none',cmap=cm.gist_heat_r,extent=(-0.5,9.5,-0.5,9.5))
axB4.set_ylabel('Keyword')
axB4.set_xlabel('Keyword')
axB4.set_xticklabels('')
axB4.set_yticklabels('')
clb5=fig4.colorbar(imB4,ax=axB4,shrink=0.4)
#%%
fig5=plt.figure(figsize=(7.5,7.5))
axA5=fig5.add_subplot(2,1,1)
sort_words_journals=matrix_words_journals[top_10_words,:]
sort_words_journals=sort_words_journals[:,top_10_journals]
sort_words_authors=matrix_words_authors[top_10_words,:]
sort_words_authors=sort_words_authors[:,top_20_authors]
imA5=axA5.imshow(sort_words_journals.T,aspect='auto',interpolation='none',cmap=cm.gist_heat_r,extent=(-0.5,9.5,-0.5,9.5))
axA5.set_xticks(np.arange(0,10))
axA5.set_xticklabels('')
axA5.set_yticks(np.arange(0,10))
axA5.set_yticklabels(np.flip(top_10_journals_name))
clb5=fig5.colorbar(imA5,ax=axA5,shrink=0.7)

axB5=fig5.add_subplot(2,1,2)
imB5=axB5.imshow(sort_words_authors.T,aspect='auto',interpolation='none',cmap=cm.gist_heat_r,extent=(-0.5,9.5,-0.5,19.5))
axB5.set_xticks(np.arange(0,10))
axB5.set_xticklabels(top_10_words_words,rotation=90)
axB5.set_yticks(np.arange(0,20))
axB5.set_yticklabels(np.flip(top_20_authors_name))
clb6=fig5.colorbar(imB5,ax=axB5,shrink=0.7)
#%%
fig6=plt.figure(figsize=(7.5,5.5))
ax6=fig6.add_subplot(1,1,1)
ax6.plot(matrix_years_words[100::,top_10_words],':P')
ax6.set_yticks(np.arange(0,125,10))
# ax6.set_yticklabels(np.flip(top_10_words_words))
ax6.set_xticks(np.arange(0,22,2))
ax6.set_xticklabels(np.arange(200,2022,2),rotation=90)
ax6.legend(top_10_words_words,fontsize=8)