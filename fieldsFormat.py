#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:28:54 2021

@author: felipe
"""

import re

def format_name(person):
    name=''
    name+=person.last_names[0]
    name+=', '
    name+=person.first_names[0]
    if person.middle_names != []:
        name+=', '
        name+=person.middle_names[0][0]+'.'
    name=re.sub('\"\{a\}','ä',name)
    name=re.sub('\"\{e\}','ë',name)
    name=re.sub('\"\{i\}','ï',name)
    name=re.sub('\"\{o\}','ö',name)
    name=re.sub('\"\{u\}','ü',name)
    name=re.sub('\'\{a\}','á',name)
    name=re.sub('\'\{e\}','é',name)
    name=re.sub('\'\{i\}','í',name)
    name=re.sub('\'\{o\}','ó',name)
    name=re.sub('\'\{u\}','ú',name)
    name=re.sub('[{\}]','',name)
    name=re.sub('[\\\]','',name)
    return name

def format_title(title):
    new_title=title.lower()
    new_title=re.sub(r'[{\)\(\}-]','',new_title)
    new_title=re.sub(r'[\'\']','',new_title)
    new_title=re.sub(r'[=]',' ',new_title)
    new_title=re.sub('\"\{a\}','ä',new_title)
    new_title=re.sub('\"\{e\}','ë',new_title)
    new_title=re.sub('\"\{i\}','ï',new_title)
    new_title=re.sub('\"\{o\}','ö',new_title)
    new_title=re.sub('\"\{u\}','ü',new_title)
    new_title=re.sub('\'\{a\}','á',new_title)
    new_title=re.sub('\'\{e\}','é',new_title)
    new_title=re.sub('\'\{i\}','í',new_title)
    new_title=re.sub('\'\{o\}','ó',new_title)
    new_title=re.sub('\'\{u\}','ú',new_title)
    new_title=re.sub('[{\}]','',new_title)
    new_title=re.sub('[\\\]','',new_title)
    return new_title
