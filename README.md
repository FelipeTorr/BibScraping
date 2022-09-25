# BibScraping
Scraping papers' data from .bib files

Requires the library pybtex


## Run

1. Execute:

 "python3 data_collection.py <MyBibiliography.bib>"

The output form this script is a file that contains the dictionaries of deducplicated authors' name, keywords, years and publishers

2. Execute:

 "python3 data_matrices.py <MyBibiliography.bib>"

 The output from this are adjacency matrices for each field (authors, keyword, years, journals)  

 3. Calculate and plot statistics of the data, an example can be found in "plotting.py" 