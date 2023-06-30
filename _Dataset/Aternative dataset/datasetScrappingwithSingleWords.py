# -*- coding: utf-8 -*-
"""
Created on Sat May  6 15:46:42 2023

@author: Idener
"""

import requests
from bs4 import BeautifulSoup
import csv
import math


# URLs of the webpages you want to extract data from
url2 = "https://www.achrafothman.net/aslsmt/corpus/sample-corpus-asl-en.asl"
url1 = "https://www.achrafothman.net/aslsmt/corpus/sample-corpus-asl-en.en"

# Make requests to the webpages and parse the HTML code with BeautifulSoup
html1 = requests.get(url1).content
soup1 = BeautifulSoup(html1, "html.parser")

html2 = requests.get(url2).content
soup2 = BeautifulSoup(html2, "html.parser")

# Find the pre elements containing the actual content in rows
pre1 = soup1
pre2 = soup2
# Split the rows of the content into a list
rows1 = pre1.text.split("\n")
rows2 = pre2.text.split("\n")

# Create a list of tuples, with each tuple containing a row from each webpage
data = list(zip(rows1, rows2))

    #crea el archivo seq2seq a raiz de las dos url del dataset original
with open("Seq2Seq.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='@')
    writer.writerow(["text", "gloss"]) # header row
    writer.writerows(data)

    #soporte para la creacion de archivos
with open("Seq2Seq.csv", "r" , encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader) # skip the header row
    lines = [row for row in reader]

    # Calculate the number of lines for the 80/20 split
    n = len(lines)
    n_80 = math.ceil(n * 0.8)
    n_20 = n - n_80
    
    # Split the lines into two sets
    set_80 = [row for row in lines[:n_80]]
    set_20 = [row for row in lines[n_80:]]
    set_20_slg = [[row] for row in rows1[n_80:]]
    set_20_eng = [[row] for row in rows2[n_80:]]

    #crea el archivo Seq2Seq80 que contiene el 80% inicial del dataset
with open("Seq2Seq80.csv", "w" , encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header) # write the header row
    writer.writerows(set_80)

with open("Seq2Seq20.csv", "w" , encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header) # write the header row
    writer.writerows(set_20)


    
def to_lower_case(s):
    return s.lower()
# Function to find common words in two lists
def common_words(list1, list2):
    return list(set(map(to_lower_case,list1)).intersection(map(to_lower_case,list2)))

# Read the Seq2Seq.csv file and store common words for each row in a set
common_words_list = []

    #Crea la lista de palabras comunes para data augmentation
with open("Seq2Seq.csv", "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter='@')
    next(reader)  # Skip header row

    for row in reader:
        gloss, text = row
        gloss_words = gloss.split()
        text_words = text.split()
        common = common_words(gloss_words, text_words)
        common_words_list = common_words_list + common 
    
    common_words_list = set(common_words_list)
    common_words_list = list(common_words_list)
        
    #Crea el archivo Seq2SeqAugmented80 que contiene las palabras y el 80% de las secuencias
with open("Seq2SeqAugmented80.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='@')
    writer.writerow(["text", "gloss"])  # header row

    # Write the common words rows
    for common_word in common_words_list:
        writer.writerow([common_word, common_word])

    # Write the original Seq2Seq80.csv content
    with open("Seq2Seq80.csv", "r", newline="", encoding="utf-8") as original_csvfile:
        original_reader = csv.reader(original_csvfile, delimiter='@')
        next(original_reader)  # Skip header row
        writer.writerows(original_reader)
        
    #Crea el archivo Seq2SeqAugmented que contiene tanto las palabras como el 100% de las secuencias
with open("Seq2SeqAugmented.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter='@')
    writer.writerow(["text", "gloss"])  # header row

    # Write the common words rows
    for common_word in common_words_list:
        writer.writerow([common_word, common_word])

    # Write the original Seq2Seq80.csv content
    with open("Seq2Seq.csv", "r", newline="", encoding="utf-8") as original_csvfile:
        original_reader = csv.reader(original_csvfile, delimiter='@')
        next(original_reader)  # Skip header row
        writer.writerows(original_reader)

